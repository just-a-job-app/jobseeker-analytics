import datetime
import logging
import json
from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks
from fastapi.responses import RedirectResponse, HTMLResponse
from google_auth_oauthlib.flow import Flow

from db.utils.user_utils import user_exists
from utils.auth_utils import AuthenticatedUser
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
async def login(request: Request, background_tasks: BackgroundTasks, db_session: database.DBSession):
    """Handles Google OAuth2 login and authorization code exchange."""
    code = request.query_params.get("code")
    client_config = {
        "web": {
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
            "redirect_uris": json.loads(os.getenv("GOOGLE_CLIENT_REDIRECT_URI")),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }
    }

    flow = Flow.from_client_config(
        client_config,
        settings.GOOGLE_SCOPES,
        redirect_uri=settings.REDIRECT_URI,
    )

    try:
        if not code:
            authorization_url, state = flow.authorization_url(prompt="consent")
            return RedirectResponse(url=authorization_url)
        logger.info("Authorization code received, exchanging for token...")
        try:
            flow.fetch_token(code=code)
        except Exception as e:
            logger.error("Failed to fetch token: %s", e)
            return RedirectResponse(
                url=f"{settings.APP_URL}/errors?message=permissions_error",
                status_code=303
            )   
        try:
            creds = flow.credentials
        except Exception as e:
            logger.error("Failed to fetch credentials: %s", e)
            return RedirectResponse(
                url=f"{settings.APP_URL}/errors?message=credentials_error",
                status_code=303
            )  

        if not creds.valid:
            creds.refresh(Request())
            return RedirectResponse("/login", status_code=303)

        user = AuthenticatedUser(creds)
        session_id = request.session["session_id"] = create_random_session_string()

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
        request.session["creds"] = creds.to_json() 
        request.session["access_token"] = creds.token

        # NOTE: change redirection once dashboard is completed
        exists, last_fetched_date = user_exists(user, db_session)
        logger.info("User exists: %s, Last fetched date: %s", exists, last_fetched_date)
        if exists:
            logger.info("User already exists in the database.")
            response = RedirectResponse(
                url=f"{settings.APP_URL}/processing", status_code=303
            )
            logger.info("Settings.is_publicly_deployed: %s", settings.is_publicly_deployed)
            logger.info("IS_DOCKER_CONTAINER: %s", os.environ.get("IS_DOCKER_CONTAINER"))
            
            background_tasks.add_task(fetch_emails_to_db, user, request, last_fetched_date, user_id=user.user_id, db_session=db_session)
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
async def logout(request: Request):
    logger.info("Logging out")
    
    # Check if user had an Authorization cookie (indicates they've ever authenticated)
    has_ever_authenticated = False
    if settings.is_publicly_deployed:
        auth_cookie = request.cookies.get("__Secure-Authorization")
    else:
        auth_cookie = request.cookies.get("Authorization")
    
    logger.info(f"[Logout] Auth cookie value: {auth_cookie}")
    has_ever_authenticated = bool(auth_cookie)
    logger.info(f"[Logout] Has ever authenticated: {has_ever_authenticated}")
    
    # Clear the session
    request.session.clear()
    logger.info("[Logout] Session cleared")
    
    # Keep Authorization cookie for returning users, remove it for first-time users
    if has_ever_authenticated:
        # Set a persistent Authorization cookie with a placeholder value
        persistent_auth_value = "logged_out"
        logger.info(f"[Logout] Setting cookie to: {persistent_auth_value}")
        response = RedirectResponse(f"{APP_URL}", status_code=303)
        response = set_conditional_cookie(
            key="Authorization", value=persistent_auth_value, response=response
        )
        logger.info("[Logout] Cookie set, returning response")
        return response
    else:
        logger.info("[Logout] No auth cookie found, deleting cookies")
        response = RedirectResponse(f"{APP_URL}", status_code=303)
        response.delete_cookie(key="__Secure-Authorization")
        response.delete_cookie(key="Authorization")
        return response


@router.get("/me")
async def getUser(request: Request, user_id: str = Depends(validate_session)):
    if not user_id:
        raise HTTPException(
            status_code=401, detail="No user id found in session"
        )    
    return {"user_id": user_id}