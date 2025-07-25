# app/session/session_layer.py
import logging
import secrets
from datetime import datetime
from fastapi import Request
from utils.config_utils import get_settings
import database
from db.users import Users
from sqlmodel import select, Session
from database import engine

settings = get_settings()


def create_random_session_string() -> str:
    return secrets.token_urlsafe(32)  # Generates a random URL-safe string


def clear_session(request: Request, user_id: str) -> None:
    logging.info("user_id: %s clear_session" % user_id)
    request.cookies.clear()


def validate_session(request: Request, db_session: database.DBSession) -> str:
    """Retrieves Authorization, session_id, access_token and token_expiry
    from request cookies and validates them.
    Session ID should match the stored session.
    Access token should not be expired.
    """
    if settings.is_publicly_deployed:
        session_authorization = request.cookies.get("__Secure-Authorization")
    else:
        session_authorization = request.cookies.get("Authorization")

    session_id = request.session.get("session_id")
    session_access_token = request.session.get("access_token")
    token_exp = request.session.get("token_expiry")
    user_id = request.session.get("user_id")
    is_demo_user = request.session.get("is_demo_user", False)

    # Handle demo users - they don't need Google authentication
    if is_demo_user and user_id:
        logging.info("Demo user session validated: %s", user_id)
        return user_id

    if not session_authorization and not session_access_token:
        logging.info(
            "No Authorization and access_token in session, redirecting to login"
        )
        return ""

    if session_authorization != session_id:
        logging.info("Authorization does not match Session Id, redirecting to login")
        return ""

    if is_token_expired(token_exp):
        logging.info("Access_token is expired, redirecting to login")
        return ""

    if user_id:
        # check that user actually exists in database first
        with Session(engine) as session:
            user = session.exec(select(Users).where(Users.user_id == user_id))
            if not user:
                clear_session(request, user_id)
                logging.info("user_id: %s deleted, redirecting to login" % user_id)
                return ""

    logging.info("Valid Session, Access granted.")
    return user_id


def is_token_expired(iso_expiry: str) -> bool:
    """
    Converts ISO format timestamp (which serves as the expiry time of the token) to datetime.
    If the current time is greater than the expiry time,
    the token is expired.
    """
    if iso_expiry:
        datetime_expiry = datetime.fromisoformat(iso_expiry)  # UTC time
        difference_in_minutes = (
            datetime_expiry - datetime.utcnow()
        ).total_seconds() / 60
        return difference_in_minutes <= 0

    return True
