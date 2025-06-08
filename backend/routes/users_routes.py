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

        index = 0

        # Tracks all job titles and their index in response_rate
        job_titles = {}

        # Store (company, job_title) tuples to avoid duplicates
        companies = []

        # List of dictionaries to store job titles and their response rates
        response_rate_data = []

        for email in user_emails:
            if email.job_title not in job_titles:
                status = email.application_status.strip().lower()
                if status == "request for availability" or status == "offer" or status == "interview scheduled":
                    response_rate_data.append({"title": email.job_title, "responses": 1, "total": 1})
                else:
                    response_rate_data.append({"title": email.job_title, "responses": 0, "total": 1})
                companies.append((email.company_name, email.job_title))
                job_titles[email.job_title] = index
                index += 1
            elif (email.company_name, email.job_title) not in companies:
                status = email.application_status.strip().lower()
                if status == "request for availability" or status == "offer" or status == "interview scheduled":
                    response_rate_data[job_titles[email.job_title]]["responses"] += 1
                response_rate_data[job_titles[email.job_title]]["total"] += 1
                companies.append((email.company_name, email.job_title))

        response_rate = []
        for data in response_rate_data:
            response_rate.append({
                "title": data["title"],
                "rate": round(data["responses"] / data["total"] * 100, 2)
            })

        return response_rate
    
    except Exception as e:
        logger.error(f"Error fetching job titles for user_id {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/user-response-rate")
def calculate_response_rate(
    request: Request, db_session: database.DBSession, user_id: str = Depends(validate_session)
) -> None:
    user_emails = db_session.exec(
        select(UserEmails).where(UserEmails.user_id == user_id)
    ).all()

    # if user has no application just return 0.0
    total_apps = len(user_emails)
    if total_apps == 0:
        return 0.0

    interview_requests = 0
    for email in user_emails:
        # using request for avalability as an interview request as it should come before the offer and scheduled interview
        if (
            email.application_status
            and email.application_status.lower() == "request for availability"
        ):
            interview_requests += 1

    response_rate_percent = (interview_requests / total_apps) * 100
    return {"value": round(response_rate_percent, 1)}
    
