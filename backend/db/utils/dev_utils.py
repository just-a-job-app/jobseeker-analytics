import logging
from sqlmodel import Session, delete
from database import engine
from db.users import Users
from db.user_emails import UserEmails
from db.companies import Companies
from db.processing_tasks import TaskRuns
from utils.config_utils import get_settings

logger = logging.getLogger(__name__)

def clear_local_database():
    """
    Clears all relevant tables in the database for local development.
    This function should only be called in development environment.
    """
    settings = get_settings()
    if settings.is_publicly_deployed:
        logger.warning("Attempted to clear database in production/staging environment. Skipping.")
        return

    logger.info("Clearing local database tables...")
    with Session(engine) as session:
        # Delete all records from each table
        session.execute(delete(UserEmails))
        session.execute(delete(TaskRuns))
        session.execute(delete(Users))
        session.execute(delete(Companies))
        session.commit()
    logger.info("Local database cleared successfully.") 