import os
from celery import Celery
from utils.config_utils import get_settings
import logging

logger = logging.getLogger(__name__)

# Get settings
settings = get_settings()

# Determine Redis URL based on environment
if os.environ.get("IS_DOCKER_CONTAINER"):
    REDIS_URL = "redis://redis:6379/0"
else:
    REDIS_URL = "redis://localhost:6379/0"

# Create Celery instance
celery_app = Celery(
    "jobseeker_analytics",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["tasks.email_tasks"]  # Import task modules
)

# Celery configuration
celery_app.conf.update(
    task_track_started=True,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    result_expires=3600,  # Results expire after 1 hour
    task_acks_late=True,  # Tasks acknowledged after completion
    worker_prefetch_multiplier=1,  # One task at a time per worker
    task_routes={
        "tasks.email_tasks.*": {"queue": "email_processing"},
    },
    task_default_queue="default",
    task_default_exchange="default",
    task_default_routing_key="default",
)

# Configure task retry settings
celery_app.conf.task_annotations = {
    "*": {
        "rate_limit": "10/m",  # Max 10 tasks per minute
        "max_retries": 3,
        "default_retry_delay": 60,  # Retry after 60 seconds
    }
}

logger.info(f"Celery app configured with broker: {REDIS_URL}")