import logging
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlmodel import select
from db.user_emails import UserEmails
from utils.config_utils import get_settings
from session.session_layer import validate_session
from routes.email_routes import query_emails
import database
from slowapi import Limiter
from slowapi.util import get_remote_address


# Logger setup
logger = logging.getLogger(__name__)

# Get settings
settings = get_settings()
APP_URL = settings.APP_URL

api_call_finished = False

# FastAPI router for email routes
router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.get("/get-response-rate")   
@limiter.limit("2/minute")    
def response_rate_by_job_title(request: Request, db_session: database.DBSession, user_id: str = Depends(validate_session)):
    
    try:
        # Get job related email data from DB
        user_emails = query_emails(request, db_session=db_session, user_id=user_id)

        # Create unique application IDs based on company_name only (ignore job_title for now)
        applications = {}
        
        for email in user_emails:
            if email.company_name:
                app_id = email.company_name  # Use only company name as unique identifier
                
                if app_id not in applications:
                    applications[app_id] = {
                        "company": email.company_name,
                        "job_title": email.job_title,
                        "statuses": set()
                    }
                
                if email.application_status:
                    status = email.application_status.strip().lower()
                    # Ignore "unknown" statuses
                    if status != "unknown":
                        applications[app_id]["statuses"].add(status)

        # Filter out applications that only have unknown statuses (no valid statuses)
        valid_applications = {}
        for app_id, app_data in applications.items():
            if app_data["statuses"]:  # Only include applications that have at least one valid status
                valid_applications[app_id] = app_data

        # Group applications by job title
        job_title_applications = {}
        
        for app_id, app_data in valid_applications.items():
            job_title = app_data["job_title"]
            
            # Skip applications with "unknown" job titles
            if job_title and job_title.lower() != "unknown":
                if job_title not in job_title_applications:
                    job_title_applications[job_title] = {
                        "total": 0,
                        "responses": 0
                    }
                
                job_title_applications[job_title]["total"] += 1
                
                # Check if this application received any response beyond initial confirmation/rejection
                statuses = app_data["statuses"]
                has_response = any(status not in ["application confirmation", "rejection"] for status in statuses)
                
                if has_response:
                    job_title_applications[job_title]["responses"] += 1

        # Calculate response rates for each job title
        response_rate = []
        for job_title, data in job_title_applications.items():
            rate = round((data["responses"] / data["total"]) * 100, 2)
            response_rate.append({
                "title": job_title,
                "rate": rate
            })

        return response_rate
    
    except Exception as e:
        logger.error(f"Error fetching job titles for user_id {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/user-response-rate")
def calculate_response_rate(
    request: Request, db_session: database.DBSession, user_id: str = Depends(validate_session)
) -> dict:
    user_emails = db_session.exec(
        select(UserEmails).where(UserEmails.user_id == user_id)
    ).all()

    # if user has no emails just return 0.0
    if not user_emails:
        return {"value": 0.0}

    # Create unique application IDs based on company_name only (ignore job_title for now)
    applications = {}
    
    logger.info(f"DEBUG: Processing {len(user_emails)} total emails")
    
    for email in user_emails:
        if email.company_name:
            app_id = email.company_name  # Use only company name as unique identifier
            
            logger.info(f"DEBUG: Email from {email.company_name} - {email.job_title} - Status: {email.application_status}")
            
            if app_id not in applications:
                applications[app_id] = {
                    "company": email.company_name,
                    "job_title": email.job_title,
                    "statuses": set(),
                    "received_at": email.received_at
                }
            
            if email.application_status:
                status = email.application_status.strip().lower()
                # Ignore "unknown" statuses
                if status != "unknown":
                    applications[app_id]["statuses"].add(status)

    logger.info(f"DEBUG: All applications before filtering: {len(applications)}")
    for app_id, app_data in applications.items():
        logger.info(f"DEBUG:   {app_id} - Statuses: {list(app_data['statuses'])}")

    # Filter out applications that only have unknown statuses (no valid statuses)
    valid_applications = {}
    for app_id, app_data in applications.items():
        if app_data["statuses"]:  # Only include applications that have at least one valid status
            valid_applications[app_id] = app_data

    # Calculate response rate
    total_applications = len(valid_applications)
    if total_applications == 0:
        return {"value": 0.0}

    # Count applications that received a response (not just application confirmation or rejection)
    responses_received = 0
    
    # Debug logging
    logger.info(f"DEBUG: Total valid applications: {total_applications}")
    
    for app_id, app_data in valid_applications.items():
        statuses = app_data["statuses"]
        company = app_data["company"]
        job_title = app_data["job_title"]
        
        # Check if this application received any response beyond initial confirmation/rejection
        has_response = any(status not in ["application confirmation", "rejection"] for status in statuses)
        
        logger.info(f"DEBUG: Application {app_id} ({company} - {job_title})")
        logger.info(f"DEBUG:   Statuses: {list(statuses)}")
        logger.info(f"DEBUG:   Has response: {has_response}")
        
        if has_response:
            responses_received += 1

    logger.info(f"DEBUG: Total responses received: {responses_received}")
    logger.info(f"DEBUG: Response rate calculation: {responses_received}/{total_applications} = {(responses_received/total_applications)*100}%")

    response_rate_percent = (responses_received / total_applications) * 100
    return {"value": round(response_rate_percent, 1)}
    
