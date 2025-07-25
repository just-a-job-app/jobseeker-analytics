"""
Utility functions for managing test emails in the database.
"""

import logging
from typing import List, Optional
from sqlmodel import Session, select
from db.test_emails import TestEmails
from tests.test_email_data import get_demo_emails, get_all_test_emails
import database

logger = logging.getLogger(__name__)

def create_test_email(user_id: str, email_data: dict) -> Optional[TestEmails]:
    """
    Creates a TestEmail record in the database.
    """
    try:
        test_email = TestEmails(
            id=email_data["id"],
            user_id=user_id,
            company_name=email_data["company_name"],
            application_status=email_data["application_status"],
            received_at=email_data["received_at"],
            subject=email_data["subject"],
            job_title=email_data["job_title"],
            email_from=email_data["email_from"],
            email_body=email_data["email_body"],
            is_demo_email=email_data.get("is_demo_email", False),
            category=email_data.get("category"),
            tags=email_data.get("tags"),
            notes=email_data.get("notes")
        )
        return test_email
    except Exception as e:
        logger.error(f"Error creating test email record: {e}")
        return None

def check_test_email_exists(user_id: str, email_id: str) -> bool:
    """
    Check if a test email already exists for the user.
    """
    with Session(database.engine) as db_session:
        existing_email = db_session.exec(
            select(TestEmails).where(
                (TestEmails.id == email_id) & (TestEmails.user_id == user_id)
            )
        ).first()
        return existing_email is not None

def load_demo_emails_for_user(user_id: str) -> List[TestEmails]:
    """
    Load demo emails for a specific user.
    """
    demo_emails = get_demo_emails()
    test_email_records = []
    
    with Session(database.engine) as db_session:
        for email_data in demo_emails:
            # Check if email already exists
            if check_test_email_exists(user_id, email_data["id"]):
                logger.info(f"Demo email {email_data['id']} already exists for user {user_id}")
                continue
            
            # Create new test email record
            test_email = create_test_email(user_id, email_data)
            if test_email:
                test_email_records.append(test_email)
        
        # Batch insert all records
        if test_email_records:
            db_session.add_all(test_email_records)
            db_session.commit()
            logger.info(f"Loaded {len(test_email_records)} demo emails for user {user_id}")
    
    return test_email_records

def get_user_test_emails(user_id: str, include_demo: bool = True) -> List[TestEmails]:
    """
    Get all test emails for a user.
    """
    with Session(database.engine) as db_session:
        query = select(TestEmails).where(TestEmails.user_id == user_id)
        if not include_demo:
            query = query.where(TestEmails.is_demo_email == False)
        
        emails = db_session.exec(query).all()
        return emails

def add_custom_test_email(user_id: str, email_data: dict) -> Optional[TestEmails]:
    """
    Add a custom test email for a user.
    """
    try:
        # Generate unique ID if not provided
        if "id" not in email_data:
            import uuid
            email_data["id"] = f"custom_{uuid.uuid4().hex[:8]}"
        
        # Check if email already exists
        if check_test_email_exists(user_id, email_data["id"]):
            logger.warning(f"Test email {email_data['id']} already exists for user {user_id}")
            return None
        
        test_email = create_test_email(user_id, email_data)
        if test_email:
            with Session(database.engine) as db_session:
                db_session.add(test_email)
                db_session.commit()
                logger.info(f"Added custom test email {email_data['id']} for user {user_id}")
                return test_email
        
        return None
    except Exception as e:
        logger.error(f"Error adding custom test email: {e}")
        return None

def delete_test_email(user_id: str, email_id: str) -> bool:
    """
    Delete a test email for a user.
    """
    try:
        with Session(database.engine) as db_session:
            email = db_session.exec(
                select(TestEmails).where(
                    (TestEmails.id == email_id) & (TestEmails.user_id == user_id)
                )
            ).first()
            
            if email:
                db_session.delete(email)
                db_session.commit()
                logger.info(f"Deleted test email {email_id} for user {user_id}")
                return True
            else:
                logger.warning(f"Test email {email_id} not found for user {user_id}")
                return False
    except Exception as e:
        logger.error(f"Error deleting test email: {e}")
        return False

def update_test_email(user_id: str, email_id: str, updates: dict) -> Optional[TestEmails]:
    """
    Update a test email for a user.
    """
    try:
        with Session(database.engine) as db_session:
            email = db_session.exec(
                select(TestEmails).where(
                    (TestEmails.id == email_id) & (TestEmails.user_id == user_id)
                )
            ).first()
            
            if email:
                # Update fields
                for key, value in updates.items():
                    if hasattr(email, key):
                        setattr(email, key, value)
                
                db_session.commit()
                logger.info(f"Updated test email {email_id} for user {user_id}")
                return email
            else:
                logger.warning(f"Test email {email_id} not found for user {user_id}")
                return None
    except Exception as e:
        logger.error(f"Error updating test email: {e}")
        return None

def search_test_emails(user_id: str, search_term: str) -> List[TestEmails]:
    """
    Search test emails by company name, subject, or email body.
    """
    with Session(database.engine) as db_session:
        query = select(TestEmails).where(
            (TestEmails.user_id == user_id) &
            (
                TestEmails.company_name.ilike(f"%{search_term}%") |
                TestEmails.subject.ilike(f"%{search_term}%") |
                TestEmails.email_body.ilike(f"%{search_term}%") |
                TestEmails.job_title.ilike(f"%{search_term}%")
            )
        )
        emails = db_session.exec(query).all()
        return emails

def get_test_email_categories() -> List[str]:
    """
    Get all available test email categories.
    """
    categories = set()
    all_emails = get_all_test_emails()
    
    for email in all_emails:
        if email.get("category"):
            categories.add(email["category"])
    
    return sorted(list(categories)) 