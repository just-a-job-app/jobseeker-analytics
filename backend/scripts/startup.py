#!/usr/bin/env python3
"""
Application Startup Script

This script runs automatically when the backend container starts.
It sets up the database, loads demo data, and ensures the application is ready.
"""

import os
import sys
import time
import logging
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from config import settings
from database import engine, create_db_and_tables
from db.utils.test_email_utils import load_demo_emails_for_user
from sqlmodel import Session
from db.users import Users
from db.test_emails import TestEmails

logger = logging.getLogger(__name__)

def wait_for_database(max_retries=30, delay=2):
    """Wait for the database to be ready."""
    logger.info("Waiting for database to be ready...")
    
    for attempt in range(max_retries):
        try:
            with Session(engine) as db_session:
                # Try a simple query to check if database is ready
                from sqlalchemy import text
                db_session.execute(text("SELECT 1"))
                logger.info("Database is ready!")
                return True
        except Exception as e:
            logger.info(f"Database not ready (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(delay)
    
    logger.error("Database failed to become ready")
    return False

def setup_database():
    """Set up the database tables."""
    logger.info("Setting up database tables...")
    try:
        create_db_and_tables()
        logger.info("Database tables created successfully")
        return True
    except Exception as e:
        logger.error(f"Error setting up database tables: {e}")
        return False

def create_default_user():
    """Create a default development user if it doesn't exist."""
    user_id = "dev_user_123"
    
    try:
        with Session(engine) as db_session:
            user = db_session.get(Users, user_id)
            if not user:
                from datetime import datetime
                user = Users(
                    user_id=user_id,
                    user_email="dev@example.com",
                    start_date=datetime.now()
                )
                db_session.add(user)
                db_session.commit()
                logger.info(f"Created default development user: {user_id}")
            else:
                logger.info(f"Default development user already exists: {user_id}")
            return user_id
    except Exception as e:
        logger.error(f"Error creating default user: {e}")
        return None

def load_demo_data(user_id):
    """Load demo emails for the development user."""
    try:
        logger.info("Loading demo emails...")
        load_demo_emails_for_user(user_id)
        
        # Verify the data was loaded
        with Session(engine) as db_session:
            test_emails = db_session.query(TestEmails).filter(TestEmails.user_id == user_id).all()
            logger.info(f"Loaded {len(test_emails)} demo emails")
        
        return True
    except Exception as e:
        logger.error(f"Error loading demo data: {e}")
        return False

def main():
    """Main startup function."""
    logger.info("🚀 Starting application setup...")
    
    # Wait for database to be ready
    if not wait_for_database():
        logger.error("❌ Failed to connect to database")
        return False
    
    # Set up database tables
    if not setup_database():
        logger.error("❌ Failed to set up database tables")
        return False
    
    # Create default user
    user_id = create_default_user()
    if not user_id:
        logger.error("❌ Failed to create default user")
        return False
    
    # Load demo data (always available for developer mode toggle)
    if not load_demo_data(user_id):
        logger.error("❌ Failed to load demo data")
        return False
    
    logger.info("🎉 Application setup complete!")
    logger.info("📖 The application is ready to use")
    logger.info("💡 Demo emails are loaded and ready for developer mode")
    logger.info("🔧 Use the 'Dev Mode' toggle in the UI to switch between real and mock Gmail API")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 