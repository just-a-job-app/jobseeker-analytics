import datetime
import logging
import json
from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks
from sqlmodel import select
from fastapi.responses import RedirectResponse, HTMLResponse
from google_auth_oauthlib.flow import Flow

from db.utils.user_utils import user_exists
from utils.auth_utils import AuthenticatedUser, get_google_authorization_url
from session.session_layer import create_random_session_string, validate_session
from utils.config_utils import get_settings
from utils.cookie_utils import set_conditional_cookie
from routes.email_routes import fetch_emails_to_db
import database
from slowapi import Limiter
from slowapi.util import get_remote_address
import os

limiter = Limiter(key_func=get_remote_address)

# Logger setup
logger = logging.getLogger(__name__)

# Get settings
settings = get_settings()

# FastAPI router for Google login
router = APIRouter()

APP_URL = settings.APP_URL


@router.get("/login")
@limiter.limit("10/minute")
async def login(
    request: Request, background_tasks: BackgroundTasks, db_session: database.DBSession
):
    """Handles Google OAuth2 login and authorization code exchange."""
    code = request.query_params.get("code")
    client_config = {
        "web": {
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
            "redirect_uris": json.loads(os.getenv("GOOGLE_CLIENT_REDIRECT_URI")),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }

    flow = Flow.from_client_config(
        client_config,
        settings.GOOGLE_SCOPES,
        redirect_uri=settings.REDIRECT_URI,
    )

    try:
        if not code:
            # Check if we have a refresh token in session
            has_refresh_token = False
            if creds_json := request.session.get("creds"):
                try:
                    creds_dict = json.loads(creds_json)
                    has_refresh_token = bool(creds_dict.get("refresh_token"))
                except json.JSONDecodeError:
                    logger.info("Trouble loading credentials from user session.")

            authorization_url, state = get_google_authorization_url(
                flow, has_refresh_token
            )
            return RedirectResponse(url=authorization_url)
        logger.info("Authorization code received, exchanging for token...")
        try:
            flow.fetch_token(code=code)
        except Exception as e:
            logger.error("Failed to fetch token: %s", e)
            return RedirectResponse(
                url=f"{settings.APP_URL}/errors?message=permissions_error",
                status_code=303,
            )
        try:
            creds = flow.credentials
            logger.info(
                "Credentials received - has refresh_token: %s",
                bool(creds.refresh_token),
            )
        except Exception as e:
            logger.error("Failed to fetch credentials: %s", e)
            return RedirectResponse(
                url=f"{settings.APP_URL}/errors?message=credentials_error",
                status_code=303,
            )

        if not creds.valid:
            try:
                creds.refresh(Request())
            except Exception as e:
                logger.error("Failed to refresh credentials: %s", e)
                # Clear expired credentials from session
                request.session.pop("creds", None)
                return RedirectResponse("/login", status_code=303)

        user = AuthenticatedUser(creds)
        # Preserve existing session_id or create new one if none exists
        session_id = request.session.get("session_id") or create_random_session_string()
        request.session["session_id"] = session_id

        # Set session details
        try:
            token_expiry = creds.expiry.isoformat()
        except Exception as e:
            logger.error("Failed to parse token expiry: %s", e)
            token_expiry = (
                datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            ).isoformat()

        request.session["token_expiry"] = token_expiry
        request.session["user_id"] = user.user_id
        if user.user_email:
            request.session["user_email"] = user.user_email
        request.session["access_token"] = creds.token

        # Preserve old refresh token if new credentials don't have one
        new_creds_json = creds.to_json()
        if not creds.refresh_token and (old_creds := request.session.get("creds")):
            try:
                old_dict = json.loads(old_creds)
                if old_dict.get("refresh_token"):
                    new_dict = json.loads(new_creds_json)
                    new_dict["refresh_token"] = old_dict["refresh_token"]
                    new_creds_json = json.dumps(new_dict)
            except json.JSONDecodeError as e:
                logger.warning(
                    "Failed to preserve refresh token from old credentials: %s", str(e)
                )

        request.session["creds"] = new_creds_json

        # NOTE: change redirection once dashboard is completed
        exists, last_fetched_date = user_exists(user, db_session)
        logger.info("User exists: %s, Last fetched date: %s", exists, last_fetched_date)
        if exists:
            logger.info("User already exists in the database.")
            response = RedirectResponse(
                url=f"{settings.APP_URL}/processing", status_code=303
            )
            logger.info(
                "Settings.is_publicly_deployed: %s", settings.is_publicly_deployed
            )
            logger.info(
                "IS_DOCKER_CONTAINER: %s", os.environ.get("IS_DOCKER_CONTAINER")
            )

            background_tasks.add_task(
                fetch_emails_to_db,
                user,
                request,
                last_fetched_date,
                user_id=user.user_id,
                db_session=db_session,
            )
            logger.info("Background task started for user_id: %s", user.user_id)
        else:
            request.session["is_new_user"] = True
            response = RedirectResponse(
                url=f"{settings.APP_URL}/dashboard", status_code=303
            )
            print("User does not exist")

        response = set_conditional_cookie(
            key="Authorization", value=session_id, response=response
        )

        return response
    except Exception as e:
        logger.error("Login error: %s", e)
        return HTMLResponse(content="An error occurred, sorry!", status_code=500)


@router.get("/logout")
async def logout(request: Request, response: RedirectResponse):
    logger.info("Logging out")
    request.session.clear()
    response.delete_cookie(key="__Secure-Authorization")
    response.delete_cookie(key="Authorization")
    return RedirectResponse(f"{APP_URL}", status_code=303)


@router.get("/me")
async def getUser(request: Request, db_session: database.DBSession, user_id: str = Depends(validate_session)):
    if not user_id:
        raise HTTPException(status_code=401, detail="No user id found in session")
    # Fetch role for user
    from db.users import Users
    user = db_session.exec(select(Users).where(Users.user_id == user_id)).first()
    role = user.role if user else "jobseeker"
    return {"user_id": user_id, "role": role}
