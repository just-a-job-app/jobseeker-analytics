import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlmodel import select, and_
from pydantic import BaseModel
from datetime import datetime
import uuid

from db.user_emails import UserEmails
from session.session_layer import validate_session
from utils.admin_utils import get_context_user_id
import database
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
logger = logging.getLogger(__name__)

router = APIRouter()

# Request/Response models
class JobApplicationCreate(BaseModel):
    company_name: str
    application_status: str
    received_at: datetime
    subject: str
    job_title: str
    email_from: str = ""

class JobApplicationUpdate(BaseModel):
    company_name: Optional[str] = None
    application_status: Optional[str] = None
    received_at: Optional[datetime] = None
    subject: Optional[str] = None
    job_title: Optional[str] = None
    email_from: Optional[str] = None

class JobApplicationResponse(BaseModel):
    id: str
    company_name: str
    application_status: str
    received_at: datetime
    subject: str
    job_title: str
    email_from: str

@router.post("/job-applications", response_model=JobApplicationResponse)
@limiter.limit("10/minute")
async def create_job_application(
    request: Request,
    application: JobApplicationCreate,
    db_session: database.DBSession,
    user_id: str = Depends(validate_session)
):
    """
    Create a new job application manually.
    """
    try:
        logger.info(f"Creating job application for user_id: {user_id}")
        
        # Generate a unique ID for the manual application
        manual_app_id = f"manual_{uuid.uuid4().hex[:8]}_{int(datetime.now().timestamp())}"
        
        # Create new UserEmails record (which serves as job application record)
        new_application = UserEmails(
            id=manual_app_id,
            user_id=user_id,
            company_name=application.company_name,
            application_status=application.application_status,
            received_at=application.received_at,
            subject=application.subject,
            job_title=application.job_title,
            email_from=application.email_from or "Manually Added"
        )
        
        db_session.add(new_application)
        db_session.commit()
        db_session.refresh(new_application)
        
        logger.info(f"Successfully created job application with id: {manual_app_id}")
        
        return JobApplicationResponse(
            id=new_application.id,
            company_name=new_application.company_name,
            application_status=new_application.application_status,
            received_at=new_application.received_at,
            subject=new_application.subject,
            job_title=new_application.job_title,
            email_from=new_application.email_from
        )
        
    except Exception as e:
        logger.error(f"Error creating job application for user_id {user_id}: {e}")
        db_session.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.put("/job-applications/{application_id}", response_model=JobApplicationResponse)
@limiter.limit("10/minute")
async def update_job_application(
    request: Request,
    application_id: str,
    application_update: JobApplicationUpdate,
    db_session: database.DBSession,
    user_id: str = Depends(validate_session)
):
    """
    Update an existing job application.
    """
    try:
        logger.info(f"Updating job application {application_id} for user_id: {user_id}")
        
        # Find the existing application
        statement = select(UserEmails).where(
            and_(UserEmails.id == application_id, UserEmails.user_id == user_id)
        )
        existing_application = db_session.exec(statement).first()
        
        if not existing_application:
            raise HTTPException(
                status_code=404, 
                detail=f"Job application with id {application_id} not found"
            )
        
        # Update only the fields that were provided
        update_data = application_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(existing_application, field, value)
        
        db_session.add(existing_application)
        db_session.commit()
        db_session.refresh(existing_application)
        
        logger.info(f"Successfully updated job application with id: {application_id}")
        
        return JobApplicationResponse(
            id=existing_application.id,
            company_name=existing_application.company_name,
            application_status=existing_application.application_status,
            received_at=existing_application.received_at,
            subject=existing_application.subject,
            job_title=existing_application.job_title,
            email_from=existing_application.email_from
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating job application {application_id} for user_id {user_id}: {e}")
        db_session.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/job-applications/{application_id}", response_model=JobApplicationResponse)
@limiter.limit("10/minute")
async def get_job_application(
    request: Request,
    application_id: str,
    db_session: database.DBSession,
    user_id: str = Depends(get_context_user_id)
):
    """
    Get a specific job application by ID.
    """
    try:
        logger.info(f"Fetching job application {application_id} for user_id: {user_id}")
        
        statement = select(UserEmails).where(
            and_(UserEmails.id == application_id, UserEmails.user_id == user_id)
        )
        application = db_session.exec(statement).first()
        
        if not application:
            raise HTTPException(
                status_code=404, 
                detail=f"Job application with id {application_id} not found"
            )
        
        return JobApplicationResponse(
            id=application.id,
            company_name=application.company_name,
            application_status=application.application_status,
            received_at=application.received_at,
            subject=application.subject,
            job_title=application.job_title,
            email_from=application.email_from
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching job application {application_id} for user_id {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/job-applications", response_model=List[JobApplicationResponse])
@limiter.limit("10/minute")
async def get_job_applications(
    request: Request,
    db_session: database.DBSession,
    user_id: str = Depends(get_context_user_id),
    status: Optional[str] = None,
    company: Optional[str] = None
):
    """
    Get all job applications for the user with optional filters.
    """
    try:
        logger.info(f"Fetching job applications for user_id: {user_id}")
        
        # Build query with filters
        statement = select(UserEmails).where(UserEmails.user_id == user_id)
        
        if status:
            statement = statement.where(UserEmails.application_status == status)
        
        if company:
            statement = statement.where(UserEmails.company_name.ilike(f"%{company}%"))
        
        # Filter out "unknown" status and order by date
        statement = statement.where(
            UserEmails.application_status.notin_(["unknown", "Unknown"])
        ).order_by(UserEmails.received_at.desc())
        
        applications = db_session.exec(statement).all()
        
        logger.info(f"Found {len(applications)} job applications for user_id: {user_id}")
        
        return [
            JobApplicationResponse(
                id=app.id,
                company_name=app.company_name,
                application_status=app.application_status,
                received_at=app.received_at,
                subject=app.subject,
                job_title=app.job_title,
                email_from=app.email_from
            )
            for app in applications
        ]
        
    except Exception as e:
        logger.error(f"Error fetching job applications for user_id {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
