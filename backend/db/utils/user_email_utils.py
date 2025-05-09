from db.user_emails import UserEmails
from datetime import datetime, timezone
import email.utils
import logging
from database import engine
from sqlmodel import Session, select
import string

logger = logging.getLogger(__name__)

def parse_email_date(date_str: str) -> datetime:
    """
    Converts an email date string into a Python datetime object
    """
    dt = email.utils.parsedate_to_datetime(date_str)
    if dt is None:
        # default to current UTC datetime
        dt = datetime.now(timezone.utc)
    return dt


def check_email_exists(user_id: str, email_id: str) -> bool:
    """
    Checks if an email with the given emailId and userId exists in the database.
    """
    with Session(engine) as session:
        statement = select(UserEmails).where(
            (UserEmails.user_id == user_id) & (UserEmails.id == email_id)
        )
        result = session.exec(statement).first()
        return result is not None


def create_user_email(user, message_data: dict) -> UserEmails:
    """
    Creates a UserEmail record instance from the provided data.
    """
    try:
        received_at_str = message_data["received_at"]
        received_at = parse_email_date(received_at_str)  # parse_email_date function was created as different date formats were being pulled from the data
        if check_email_exists(user.user_id, message_data["id"]):
            logger.info(f"Email with ID {message_data['id']} already exists in the database.")
            return None
        return UserEmails(
            id=message_data["id"],
            user_id=user.user_id,
            company_name=message_data["company_name"],
            application_status=message_data["application_status"],
            received_at=received_at,
            subject=message_data["subject"],
            job_title=message_data["job_title"],
            email_from=message_data["from"]
        )
    except Exception as e:
        logger.error(f"Error creating UserEmail record: {e}")
        return None

def clean_email_prefix(email: str) -> str:
    prefix = email.split('@')[0]
    # Remove punctuation and whitespace, convert to lowercase
    return ''.join(c for c in prefix if c not in string.punctuation).replace(" ", "").lower()

def email_is_similar(user_email: str, logged_in_user_email: str) -> bool:
    """
    Checks if the email "from" field contains similarities to the user's email address before the domain name and skips processing if so.
    Remove spaces and convert to lowercase for comparison.
    Remove punctuation from the email prefix for comparison.
    """
    try:
        user_email_prefix = clean_email_prefix(user_email)
        logged_in_user_email_prefix = clean_email_prefix(logged_in_user_email)
        import pdb; pdb.set_trace()
        return user_email_prefix == logged_in_user_email_prefix
    except Exception as e:
        logger.error(f"Error comparing email prefixes: {e}")
        return False