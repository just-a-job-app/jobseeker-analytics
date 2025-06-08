import logging
from typing import Optional, Tuple
from db.user_emails import UserEmails
from sqlmodel import Session, select, func
from db.users import Users 
from datetime import datetime, timedelta, timezone 

logger = logging.getLogger(__name__)

def get_last_email_date(user_id: str) -> Optional[datetime]:
    from database import engine
    """
    Checks date of user's most recent email 

    """
    with Session(engine) as session:
        row = session.exec(
            select(func.max(UserEmails.received_at))
            .where(UserEmails.user_id == user_id)
        ).one() # aggregates in SQL to a single row
    return row

def user_exists(user) -> Tuple[bool, Optional[datetime]]:
    from database import engine
    """
    Checks if user is already in the database

    """
    with Session(engine) as session:
        existing_user = session.exec(select(Users).where(Users.user_id == user.user_id)).first()
        if not existing_user:
            return False, None
        else:
            last_fetched_date = get_last_email_date(user.user_id)
            return True, last_fetched_date

def add_user(user, request, start_date=None) -> Users:
    """
    Writes user data to the users model and session storage

    """
    from database import engine
    with Session(engine) as session:
        # Check if the user already exists in the database
        existing_user = session.exec(select(Users).where(Users.user_id == user.user_id)).first()

        if not existing_user:

            start_date = getattr(user, "start_date", None) or (datetime.now(timezone.utc) - timedelta(days=90))

            if isinstance(start_date, datetime):
                start_date = start_date.strftime("%Y-%m-%d")

            # add a new user record
            new_user = Users(
                user_id=user.user_id,
                user_email=user.user_email,
                start_date=start_date
            )

            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            logger.info(f"Created new user record for user_id: {user.user_id}")

            # Write start date to session storage
            if isinstance(start_date, str):
                request.session["start_date"] = start_date  # Already a string, no need to convert
            else:
                request.session["start_date"] = start_date.isoformat()  # Convert only if it's a datetime object

            return new_user
        else:
            logger.info(f"User {user.user_id} already exists in the database.")
            return existing_user