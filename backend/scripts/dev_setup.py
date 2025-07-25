#!/usr/bin/env python3
"""
Development Setup Script for JobSeeker Analytics

This script helps developers quickly set up the demo environment
without needing to configure real Gmail API credentials.

Usage:
    python scripts/dev_setup.py [user_id]
"""

import sys
import os
import argparse
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from config import get_settings
from db.utils.test_email_utils import load_demo_emails_for_user, get_user_test_emails
from database import engine
from sqlmodel import Session
from db.users import Users
from db.user_emails import UserEmails
from db.test_emails import TestEmails

def setup_dev_environment(user_id: str = None):
    """Set up the development environment with demo data."""
    settings = get_settings()
    
    print("🚀 Setting up development environment...")
    
    # Check if we're in development mode
    if not settings.is_demo_mode:
        print("⚠️  Warning: Not in development mode. Set ENV=dev or DEMO_MODE=True")
        print("   This script works best in development mode.")
    
    # Create a default user if none provided
    if not user_id:
        user_id = "dev_user_123"
        print(f"📝 Using default user ID: {user_id}")
    
    try:
        # Create user if it doesn't exist
        with Session(engine) as db_session:
            user = db_session.get(Users, user_id)
            if not user:
                user = Users(
                    user_id=user_id,
                    user_email="dev@example.com",
                    first_name="Developer",
                    last_name="User",
                    created_at=settings.current_time,
                    updated_at=settings.current_time
                )
                db_session.add(user)
                db_session.commit()
                print(f"✅ Created user: {user_id}")
            else:
                print(f"✅ User already exists: {user_id}")
        
        # Load demo emails
        print("📧 Loading demo emails...")
        load_demo_emails_for_user(user_id)
        
        # Verify the setup
        with Session(engine) as db_session:
            test_emails = get_user_test_emails(user_id, include_demo=True)
            print(f"✅ Loaded {len(test_emails)} demo emails")
            
            # Show a sample of the emails
            print("\n📋 Sample demo emails:")
            for i, email in enumerate(test_emails[:3]):
                print(f"  {i+1}. {email.company_name} - {email.application_status}")
                print(f"     Subject: {email.subject}")
                print()
        
        print("🎉 Development environment setup complete!")
        print("\n📖 Next steps:")
        print("   1. Start the backend server: python main.py")
        print("   2. Start the frontend: npm run dev")
        print("   3. Navigate to the dashboard")
        print("   4. Use the 'Dev Mode' toggle in the navbar")
        print("\n💡 The app will now use mock Gmail API calls with test data")
        
    except Exception as e:
        print(f"❌ Error setting up development environment: {e}")
        sys.exit(1)

def list_demo_emails(user_id: str = None):
    """List all demo emails for a user."""
    if not user_id:
        user_id = "dev_user_123"
    
    try:
        with Session(engine) as db_session:
            test_emails = get_user_test_emails(user_id, include_demo=True)
            
            print(f"📧 Demo emails for user {user_id}:")
            print(f"Total: {len(test_emails)} emails\n")
            
            for i, email in enumerate(test_emails):
                print(f"{i+1:2d}. {email.company_name}")
                print(f"    Status: {email.application_status}")
                print(f"    Job: {email.job_title}")
                print(f"    Subject: {email.subject}")
                print(f"    From: {email.email_from}")
                print(f"    Date: {email.received_at.strftime('%Y-%m-%d %H:%M')}")
                print(f"    Demo: {'Yes' if email.is_demo_email else 'No'}")
                print()
                
    except Exception as e:
        print(f"❌ Error listing demo emails: {e}")

def clear_demo_data(user_id: str = None):
    """Clear all demo data for a user."""
    if not user_id:
        user_id = "dev_user_123"
    
    try:
        with Session(engine) as db_session:
            # Delete test emails
            test_emails = db_session.query(TestEmails).filter(TestEmails.user_id == user_id).all()
            for email in test_emails:
                db_session.delete(email)
            
            # Delete user emails (if any)
            user_emails = db_session.query(UserEmails).filter(UserEmails.user_id == user_id).all()
            for email in user_emails:
                db_session.delete(email)
            
            # Delete user
            user = db_session.get(Users, user_id)
            if user:
                db_session.delete(user)
            
            db_session.commit()
            print(f"✅ Cleared all demo data for user: {user_id}")
            
    except Exception as e:
        print(f"❌ Error clearing demo data: {e}")

def main():
    parser = argparse.ArgumentParser(description="Development setup for JobSeeker Analytics")
    parser.add_argument("user_id", nargs="?", help="User ID to set up (default: dev_user_123)")
    parser.add_argument("--list", action="store_true", help="List demo emails")
    parser.add_argument("--clear", action="store_true", help="Clear demo data")
    
    args = parser.parse_args()
    
    if args.clear:
        clear_demo_data(args.user_id)
    elif args.list:
        list_demo_emails(args.user_id)
    else:
        setup_dev_environment(args.user_id)

if __name__ == "__main__":
    main() 