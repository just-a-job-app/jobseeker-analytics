from db import processing_tasks as task_models
from sqlmodel import Session, select
import database
import logging
from utils.config_utils import get_settings

# Logger setup
logger = logging.getLogger(__name__)
settings = get_settings()

def processed_emails_exceeds_rate_limit(user_id):
    with Session(database.engine) as db_session:
        logger.info(f"Fetching processed task count for user_id: {user_id}")
        process_task_run = db_session.exec(
            select(task_models.TaskRuns).filter_by(user_id=user_id)
        ).one_or_none()
        total_processed_tasks = process_task_run.processed_tasks or 0
        logger.info(f"Total processed tasks: {total_processed_tasks}")
        return exceeds_rate_limit(total_processed_tasks)


def exceeds_rate_limit(count: int):
    rate_limit = settings.batch_size_by_env
    if count >= rate_limit:
        logger.info(f"Rate limit exceeded: {count} >= {rate_limit}")
        return True
    else:
        logger.info(f"Rate limit not exceeded: {count} < {rate_limit}")
        return False
