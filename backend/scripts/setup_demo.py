#!/usr/bin/env python3
"""
Demo Mode Setup Script

This script helps set up demo mode for live presentations.
It loads demo emails and enables demo mode for a user.
"""

import sys
import os
import asyncio
from datetime import datetime

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.utils.test_email_utils import load_demo_emails_for_user
from database import create_db_and_tables
from sqlmodel import Session, select
from db.test_emails import TestEmails
import database

def setup_demo_mode(user_id: str = "demo_user"):
    """
    Set up demo mode for a user by loading demo emails.
    
    Args:
        user_id: The user ID to set up demo mode for
    """
    print(f"Setting up demo mode for user: {user_id}")
    
    # Create database tables if they don't exist
    create_db_and_tables()
    
    # Load demo emails for the user
    try:
        loaded_emails = load_demo_emails_for_user(user_id)
        print(f"✅ Successfully loaded {len(loaded_emails)} demo emails")
        
        # Verify the emails were loaded
        with Session(database.engine) as db_session:
            demo_emails = db_session.exec(
                select(TestEmails).where(
                    (TestEmails.user_id == user_id) & (TestEmails.is_demo_email == True)
                )
            ).all()
            
            print(f"✅ Verified {len(demo_emails)} demo emails in database")
            
            # Print summary of loaded emails
            print("\n📧 Demo Emails Loaded:")
            for email in demo_emails:
                print(f"  • {email.company_name} - {email.application_status}")
                
    except Exception as e:
        print(f"❌ Error setting up demo mode: {e}")
        return False
    
    print(f"\n🎉 Demo mode setup complete for user: {user_id}")
    print("You can now enable demo mode in the application!")
    return True

def list_demo_emails(user_id: str = "demo_user"):
    """
    List all demo emails for a user.
    
    Args:
        user_id: The user ID to list emails for
    """
    print(f"Listing demo emails for user: {user_id}")
    
    try:
        with Session(database.engine) as db_session:
            demo_emails = db_session.exec(
                select(TestEmails).where(
                    (TestEmails.user_id == user_id) & (TestEmails.is_demo_email == True)
                ).order_by(TestEmails.received_at)
            ).all()
            
            if not demo_emails:
                print("No demo emails found.")
                return
            
            print(f"\n📧 Found {len(demo_emails)} demo emails:")
            print("-" * 80)
            
            for i, email in enumerate(demo_emails, 1):
                print(f"{i:2d}. {email.company_name}")
                print(f"    Status: {email.application_status}")
                print(f"    Job: {email.job_title}")
                print(f"    Subject: {email.subject}")
                print(f"    Date: {email.received_at.strftime('%Y-%m-%d %H:%M')}")
                print(f"    Category: {email.category or 'N/A'}")
                print("-" * 80)
                
    except Exception as e:
        print(f"❌ Error listing demo emails: {e}")

def clear_demo_emails(user_id: str = "demo_user"):
    """
    Clear all demo emails for a user.
    
    Args:
        user_id: The user ID to clear emails for
    """
    print(f"Clearing demo emails for user: {user_id}")
    
    try:
        with Session(database.engine) as db_session:
            demo_emails = db_session.exec(
                select(TestEmails).where(
                    (TestEmails.user_id == user_id) & (TestEmails.is_demo_email == True)
                )
            ).all()
            
            for email in demo_emails:
                db_session.delete(email)
            
            db_session.commit()
            print(f"✅ Cleared {len(demo_emails)} demo emails")
            
    except Exception as e:
        print(f"❌ Error clearing demo emails: {e}")

def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) < 2:
        print("Usage: python setup_demo.py <command> [user_id]")
        print("\nCommands:")
        print("  setup    - Set up demo mode (load demo emails)")
        print("  list     - List all demo emails")
        print("  clear    - Clear all demo emails")
        print("\nExamples:")
        print("  python setup_demo.py setup")
        print("  python setup_demo.py setup my_user_id")
        print("  python setup_demo.py list")
        print("  python setup_demo.py clear")
        return
    
    command = sys.argv[1].lower()
    user_id = sys.argv[2] if len(sys.argv) > 2 else "demo_user"
    
    if command == "setup":
        setup_demo_mode(user_id)
    elif command == "list":
        list_demo_emails(user_id)
    elif command == "clear":
        clear_demo_emails(user_id)
    else:
        print(f"Unknown command: {command}")
        print("Available commands: setup, list, clear")

if __name__ == "__main__":
    main() 