import logging
from typing import Optional, List, Dict
from datetime import datetime, timedelta
from celery import Task
from sqlmodel import Session, select
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

from celery_app import celery_app
from database import engine
from db.users import Users
from db.user_emails import UserEmails
from db import processing_tasks as task_models
from db.utils.user_email_utils import create_user_email, check_email_exists
from utils.email_utils import get_email_ids, get_email
from utils.llm_utils import process_email
from utils.config_utils import get_settings
# Import Gemini-specific modules only if using Gemini
import os
if os.getenv("LLM_PROVIDER", "claude").lower() == "gemini":
    from utils.llm_optimization import BatchProcessor, RateLimitManager, check_pattern_cache
    from utils.gemini_retry import should_retry_task
else:
    # Dummy implementations for non-Gemini providers
    class RateLimitManager:
        def can_make_request(self): return True
        def record_request(self): pass
        def get_wait_time(self): return 0
    
    def should_retry_task(error): return False
    def check_pattern_cache(email): return None
    BatchProcessor = None
from start_date.storage import get_start_date_email_filter
from constants import QUERY_APPLIED_EMAIL_FILTER
import time

logger = logging.getLogger(__name__)
settings = get_settings()

SECONDS_BETWEEN_FETCHING_EMAILS = 1 * 60 * 60  # 1 hour


class EmailProcessingTask(Task):
    """Custom task class for email processing with better error handling"""
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Called when task fails"""
        user_id = kwargs.get('user_id')
        if user_id:
            with Session(engine) as db_session:
                process_task_run = db_session.get(task_models.TaskRuns, user_id)
                if process_task_run:
                    process_task_run.status = task_models.FINISHED
                    process_task_run.error_message = str(exc)
                    db_session.commit()
        logger.error(f"Task {task_id} failed for user {user_id}: {exc}")


@celery_app.task(bind=True, base=EmailProcessingTask, name="tasks.email_tasks.fetch_and_process_emails")
def fetch_and_process_emails(
    self,
    user_id: str,
    creds_dict: dict,
    start_date: Optional[str] = None,
    is_new_user: bool = False,
    last_updated: Optional[str] = None
) -> Dict[str, any]:
    """
    Celery task to fetch and process emails for a user.
    
    Args:
        user_id: User ID
        creds_dict: Google OAuth credentials as dict
        start_date: Optional start date for email filtering
        is_new_user: Whether this is a new user
        last_updated: ISO format string of last update time
        
    Returns:
        Dict with processing results
    """
    logger.info(f"Starting email processing task for user_id: {user_id}")
    
    with Session(engine) as db_session:
        # Get or create task run record
        process_task_run = db_session.get(task_models.TaskRuns, user_id)
        
        if process_task_run is None:
            process_task_run = task_models.TaskRuns(user_id=user_id)
            db_session.add(process_task_run)
        elif datetime.now() - process_task_run.updated < timedelta(seconds=SECONDS_BETWEEN_FETCHING_EMAILS):
            # Check if we should skip due to rate limiting
            if process_task_run.status == task_models.FINISHED:
                logger.warning(f"Less than an hour since last fetch for user {user_id}")
                return {
                    "status": "rate_limited",
                    "message": "Please wait before fetching emails again",
                    "next_allowed": (process_task_run.updated + timedelta(seconds=SECONDS_BETWEEN_FETCHING_EMAILS)).isoformat()
                }
        
        # Check if we're resuming a task
        if process_task_run.status == task_models.STARTED and process_task_run.total_emails > 0:
            # Resume from where we left off
            logger.info(f"Resuming task for user {user_id} from email {process_task_run.processed_emails}/{process_task_run.total_emails}")
            resume_from = process_task_run.processed_emails
        else:
            # Start fresh
            process_task_run.processed_emails = 0
            process_task_run.total_emails = 0
            process_task_run.status = task_models.STARTED
            process_task_run.error_message = None
            resume_from = 0
        
        # Update Celery task ID for tracking
        process_task_run.celery_task_id = self.request.id
        db_session.commit()
        
        # Reconstruct credentials
        try:
            creds = Credentials.from_authorized_user_info(creds_dict)
        except Exception as e:
            logger.error(f"Failed to reconstruct credentials: {e}")
            process_task_run.status = task_models.FINISHED
            process_task_run.error_message = "Invalid credentials"
            db_session.commit()
            return {"status": "error", "message": "Invalid credentials"}
        
        # Get user
        user = db_session.get(Users, user_id)
        if not user:
            logger.error(f"User {user_id} not found")
            process_task_run.status = task_models.FINISHED
            process_task_run.error_message = "User not found"
            db_session.commit()
            return {"status": "error", "message": "User not found"}
        
        # Build query - ALWAYS use the 90-day filter
        query = QUERY_APPLIED_EMAIL_FILTER
        
        if last_updated:
            last_updated_dt = datetime.fromisoformat(last_updated)
            additional_time = int(last_updated_dt.timestamp())
            # Only fetch emails newer than last_updated
            query += f" after:{additional_time}"
            logger.info(f"Fetching emails after {last_updated} with query: {query}")
        else:
            logger.info(f"Fetching emails from last 90 days for user {user_id} with query: {query}")
        
        # Build Gmail service
        service = build("gmail", "v1", credentials=creds)
        
        # Get email IDs
        messages = get_email_ids(query=query, gmail_instance=service)
        
        if not messages:
            logger.info(f"No emails found for user {user_id}")
            process_task_run.status = task_models.FINISHED
            db_session.commit()
            return {"status": "success", "processed": 0, "total": 0}
        
        logger.info(f"Found {len(messages)} emails for user {user_id}")
        process_task_run.total_emails = len(messages)
        db_session.commit()
        
        # Initialize batch processor and rate limiter
        if os.getenv("LLM_PROVIDER", "claude").lower() == "gemini":
            batch_processor = BatchProcessor()
            rate_limiter = RateLimitManager()
        else:
            batch_processor = None
            rate_limiter = RateLimitManager()  # Uses dummy implementation
        
        # Process emails
        email_records = []
        processed_count = 0
        skipped_count = 0
        
        for idx, message in enumerate(messages):
            # Skip already processed emails when resuming
            if idx < resume_from:
                continue
                
            msg_id = message["id"]
            
            # Update progress
            self.update_state(
                state='PROGRESS',
                meta={
                    'current': idx + 1,
                    'total': len(messages),
                    'user_id': user_id
                }
            )
            
            # Check if email already exists
            if check_email_exists(user_id, msg_id):
                logger.info(f"Email {msg_id} already exists, skipping")
                skipped_count += 1
                process_task_run.processed_emails = idx + 1
                db_session.commit()
                continue
            
            logger.info(f"Processing email {idx + 1}/{len(messages)} with id {msg_id}")
            
            try:
                # Fetch email content
                msg = get_email(message_id=msg_id, gmail_instance=service, user_email=user.user_email)
                
                if msg:
                    # Check pattern cache first
                    cached_result = check_pattern_cache(msg["text_content"])
                    
                    if cached_result:
                        # Use cached result
                        result = cached_result
                        logger.info(f"Using cached pattern for email {idx+1}")
                    else:
                        # Wait if rate limit reached (only for Gemini)
                        if os.getenv("LLM_PROVIDER", "claude").lower() == "gemini":
                            wait_time = rate_limiter.get_wait_time()
                            if wait_time > 0:
                                logger.info(f"Rate limit reached, waiting {wait_time:.1f} seconds...")
                                time.sleep(wait_time)
                        
                        # Process with LLM
                        rate_limiter.record_request()
                        result = process_email(msg["text_content"])
                    
                    # Handle empty values
                    if isinstance(result, dict):
                        for key in result.keys():
                            if not result[key]:
                                result[key] = "unknown"
                    else:
                        result = {"company_name": "unknown", "application_status": "unknown", "job_title": "unknown"}
                    
                    # Skip false positives
                    if result.get("job_application_status", "").lower().strip() == "false positive":
                        logger.info(f"Email {msg_id} is a false positive")
                        skipped_count += 1
                    else:
                        # Create email record
                        message_data = {
                            "id": msg_id,
                            "company_name": result.get("company_name", "unknown"),
                            "application_status": result.get("job_application_status", "unknown"),
                            "received_at": msg.get("date", "unknown"),
                            "subject": msg.get("subject", "unknown"),
                            "job_title": result.get("job_title", "unknown"),
                            "from": msg.get("from", "unknown"),
                        }
                        
                        email_record = create_user_email(user, message_data)
                        if email_record:
                            email_records.append(email_record)
                            processed_count += 1
                
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "quota" in error_str.lower() or "resource_exhausted" in error_str.lower():
                    # Check if we should retry
                    should_retry, wait_time = should_retry_task(error_str, 0)  # Using 0 as we handle retries differently
                    
                    if should_retry and wait_time < 300:  # Only wait if less than 5 minutes
                        logger.warning(f"Rate limit hit, waiting {wait_time:.0f} seconds...")
                        time.sleep(wait_time)
                        # Retry this email once
                        try:
                            result = process_email(msg["text_content"])
                        except Exception as retry_error:
                            logger.error(f"Failed to process email {msg_id} after retry: {retry_error}")
                            continue
                    else:
                        # Save progress and stop processing
                        logger.error(f"Rate limit requires long wait or is daily limit. Stopping processing.")
                        process_task_run.error_message = f"Rate limited: {error_str}"
                        db_session.commit()
                        break  # Exit the loop to save progress
                else:
                    logger.error(f"Error processing email {msg_id}: {e}")
                    # Continue with next email instead of failing entire task
            
            # Update progress
            process_task_run.processed_emails = idx + 1
            db_session.commit()
        
        # Batch insert all email records
        if email_records:
            db_session.add_all(email_records)
            db_session.commit()
            logger.info(f"Added {len(email_records)} email records for user {user_id}")
        
        # Mark task as finished
        process_task_run.status = task_models.FINISHED
        db_session.commit()
        
        logger.info(f"Email processing complete for user {user_id}: {processed_count} processed, {skipped_count} skipped")
        
        return {
            "status": "success",
            "processed": processed_count,
            "skipped": skipped_count,
            "total": len(messages)
        }


@celery_app.task(name="tasks.email_tasks.get_processing_status")
def get_processing_status(user_id: str) -> Dict[str, any]:
    """Get the current processing status for a user"""
    with Session(engine) as db_session:
        process_task_run = db_session.get(task_models.TaskRuns, user_id)
        
        if not process_task_run:
            return {"status": "not_started"}
        
        return {
            "status": process_task_run.status,
            "processed_emails": process_task_run.processed_emails,
            "total_emails": process_task_run.total_emails,
            "updated": process_task_run.updated.isoformat(),
            "celery_task_id": process_task_run.celery_task_id
        }