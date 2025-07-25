"""
Routes for managing test emails in demo mode and for testing purposes.
"""

import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, Request, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlmodel import Session, select, desc
from db.test_emails import TestEmails
from db.utils.test_email_utils import (
    load_demo_emails_for_user,
    get_user_test_emails,
    add_custom_test_email,
    delete_test_email,
    update_test_email,
    search_test_emails,
    get_test_email_categories
)
from utils.auth_utils import AuthenticatedUser
from utils.config_utils import get_settings
from session.session_layer import validate_session
import database
from datetime import datetime
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

# Logger setup
logger = logging.getLogger(__name__)

# Get settings
settings = get_settings()

# FastAPI router for test email routes
router = APIRouter()

@router.post("/load-demo-emails")
@limiter.limit("5/minute")
async def load_demo_emails(
    request: Request, 
    user_id: str = Depends(validate_session)
):
    """
    Load demo emails for the current user (demo mode).
    """
    if not user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    try:
        # Load demo emails for the user
        loaded_emails = load_demo_emails_for_user(user_id)
        
        return JSONResponse(content={
            "message": f"Loaded {len(loaded_emails)} demo emails",
            "loaded_count": len(loaded_emails)
        })
    except Exception as e:
        logger.error(f"Error loading demo emails for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to load demo emails: {str(e)}")

@router.get("/test-emails", response_model=List[TestEmails])
@limiter.limit("10/minute")
def get_test_emails(
    request: Request, 
    db_session: database.DBSession, 
    include_demo: bool = True
) -> List[TestEmails]:
    # Get user_id from session if available, otherwise use default
    user_id = request.session.get("user_id", "dev_user_123")
    """
    Get all test emails for the current user.
    """
    try:
        logger.info(f"Fetching test emails for user_id: {user_id}")
        
        # Query test emails sorted by date (newest first)
        statement = select(TestEmails).where(TestEmails.user_id == user_id)
        if not include_demo:
            statement = statement.where(TestEmails.is_demo_email == False)
        
        statement = statement.order_by(desc(TestEmails.received_at))
        test_emails = db_session.exec(statement).all()
        
        logger.info(f"Found {len(test_emails)} test emails for user_id: {user_id}")
        return test_emails
        
    except Exception as e:
        logger.error(f"Error fetching test emails for user_id {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.post("/add-test-email")
@limiter.limit("10/minute")
async def add_test_email(
    request: Request,
    user_id: str = Depends(validate_session)
):
    """
    Add a custom test email for the current user.
    """
    if not user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    try:
        # Get email data from request body
        email_data = await request.json()
        
        # Validate required fields
        required_fields = ["company_name", "application_status", "subject", "job_title", "email_from", "email_body"]
        for field in required_fields:
            if field not in email_data or not email_data[field]:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
        
        # Set received_at to current time if not provided
        if "received_at" not in email_data:
            email_data["received_at"] = datetime.now()
        
        # Add the test email
        test_email = add_custom_test_email(user_id, email_data)
        
        if test_email:
            return JSONResponse(content={
                "message": "Test email added successfully",
                "email_id": test_email.id
            })
        else:
            raise HTTPException(status_code=400, detail="Failed to add test email")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding test email for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to add test email: {str(e)}")

@router.delete("/delete-test-email/{email_id}")
@limiter.limit("10/minute")
async def delete_test_email_route(
    request: Request,
    email_id: str,
    user_id: str = Depends(validate_session)
):
    """
    Delete a test email for the current user.
    """
    if not user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    try:
        success = delete_test_email(user_id, email_id)
        
        if success:
            return JSONResponse(content={"message": "Test email deleted successfully"})
        else:
            raise HTTPException(status_code=404, detail="Test email not found")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting test email {email_id} for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete test email: {str(e)}")

@router.put("/update-test-email/{email_id}")
@limiter.limit("10/minute")
async def update_test_email_route(
    request: Request,
    email_id: str,
    user_id: str = Depends(validate_session)
):
    """
    Update a test email for the current user.
    """
    if not user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    try:
        # Get update data from request body
        updates = await request.json()
        
        # Update the test email
        test_email = update_test_email(user_id, email_id, updates)
        
        if test_email:
            return JSONResponse(content={
                "message": "Test email updated successfully",
                "email_id": test_email.id
            })
        else:
            raise HTTPException(status_code=404, detail="Test email not found")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating test email {email_id} for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update test email: {str(e)}")

@router.get("/search-test-emails")
@limiter.limit("10/minute")
def search_test_emails_route(
    request: Request,
    db_session: database.DBSession,
    user_id: str = Depends(validate_session),
    q: str = ""
) -> List[TestEmails]:
    """
    Search test emails by company name, subject, or email body.
    """
    try:
        if not q:
            raise HTTPException(status_code=400, detail="Search query is required")
        
        logger.info(f"Searching test emails for user_id: {user_id} with query: {q}")
        
        # Search test emails
        test_emails = search_test_emails(user_id, q)
        
        logger.info(f"Found {len(test_emails)} test emails matching query for user_id: {user_id}")
        return test_emails
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error searching test emails for user_id {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/test-email-categories")
@limiter.limit("5/minute")
def get_categories(request: Request) -> List[str]:
    """
    Get all available test email categories.
    """
    try:
        categories = get_test_email_categories()
        return categories
    except Exception as e:
        logger.error(f"Error getting test email categories: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.post("/enable-demo-mode")
@limiter.limit("5/minute")
async def enable_demo_mode(
    request: Request
):
    # Get user_id from session if available, otherwise use default
    user_id = request.session.get("user_id", "dev_user_123")
    """
    Enable demo mode for the current user by loading demo emails.
    """
    if not user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    try:
        # Load demo emails for the user
        loaded_emails = load_demo_emails_for_user(user_id)
        
        # Set demo mode flag in session
        request.session["demo_mode"] = True
        
        return JSONResponse(content={
            "message": f"Demo mode enabled. Loaded {len(loaded_emails)} demo emails",
            "loaded_count": len(loaded_emails),
            "demo_mode": True
        })
    except Exception as e:
        logger.error(f"Error enabling demo mode for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to enable demo mode: {str(e)}")

@router.post("/disable-demo-mode")
@limiter.limit("5/minute")
async def disable_demo_mode(
    request: Request
):
    # Get user_id from session if available, otherwise use default
    user_id = request.session.get("user_id", "dev_user_123")
    """
    Disable demo mode for the current user.
    """
    if not user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    try:
        # Remove demo mode flag from session
        request.session["demo_mode"] = False
        
        return JSONResponse(content={
            "message": "Demo mode disabled",
            "demo_mode": False
        })
    except Exception as e:
        logger.error(f"Error disabling demo mode for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to disable demo mode: {str(e)}")

@router.post("/setup-demo-session")
@limiter.limit("5/minute")
async def setup_demo_session(request: Request):
    """
    Set up a demo session for users who bypass Google login in developer mode.
    """
    try:
        # Use default demo user
        user_id = "dev_user_123"
        
        # Set up session data for demo user
        request.session["user_id"] = user_id
        request.session["demo_mode"] = True
        request.session["is_demo_user"] = True
        
        # Create a demo session ID
        import secrets
        session_id = secrets.token_urlsafe(32)
        request.session["session_id"] = session_id
        
        # Create response with session data
        response = JSONResponse(content={
            "message": "Demo session created successfully",
            "user_id": user_id,
            "session_id": session_id,
            "demo_mode": True
        })
        
        # Set the Authorization cookie for demo users
        from utils.cookie_utils import set_conditional_cookie
        response = set_conditional_cookie(
            key="Authorization", value=session_id, response=response
        )
        
        return response
    except Exception as e:
        logger.error(f"Error setting up demo session: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to set up demo session: {str(e)}") 