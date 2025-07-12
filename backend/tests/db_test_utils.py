#!/usr/bin/env python3
"""
Database test utilities for populating mock data for Sankey diagram testing
"""

import os
import sys
from datetime import datetime, timedelta
import uuid

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from sqlmodel import Session
    from database import engine, create_db_and_tables
    from db.users import Users
    from db.user_emails import UserEmails
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    DEPENDENCIES_AVAILABLE = False
    print("⚠️  Database dependencies not available. Install sqlmodel and other requirements to use database functions.")

def create_test_user(session, user_id: str = None, user_email: str = "sankeytest@example.com") -> str:
    """Create a test user for Sankey diagram testing"""
    if not DEPENDENCIES_AVAILABLE:
        raise ImportError("Database dependencies not available")
    
    if user_id is None:
        user_id = f"sankey_test_{uuid.uuid4().hex[:8]}"
    
    # Remove existing user if exists
    existing_user = session.get(Users, user_id)
    if existing_user:
        session.delete(existing_user)
    
    # Create new test user
    user = Users(
        user_id=user_id,
        user_email=user_email,
        start_date=datetime.now() - timedelta(days=90)
    )
    
    session.add(user)
    session.commit()
    return user_id

def create_sankey_test_emails(session, user_id: str) -> list:
    """Create specific test emails for validating Sankey diagram functionality"""
    if not DEPENDENCIES_AVAILABLE:
        raise ImportError("Database dependencies not available")
    
    # Remove existing emails for this user
    existing_emails = session.query(UserEmails).filter(UserEmails.user_id == user_id).all()
    for email in existing_emails:
        session.delete(email)
    
    # Test emails with specific status patterns that were problematic
    test_email_data = [
        # Offer variations (should be caught by new flexible matching)
        ("TechCorp", "offer made", "Senior Developer", "Job offer - Senior Developer"),
        ("StartupXYZ", "Offer made", "Full Stack Engineer", "Congratulations! Offer letter attached"),
        ("InnoLab", "pleased to offer you", "Tech Lead", "We are pleased to offer you the position"),
        
        # Rejection variations
        ("MegaCorp", "rejected", "Data Scientist", "Application status update"),
        ("CloudSoft", "Rejection", "Product Manager", "Thank you for your interest"),
        ("AI Corp", "regret to inform", "ML Engineer", "Unfortunately, we must inform you"),
        
        # Availability variations
        ("DevTools", "Availability request", "DevOps Engineer", "Please share your availability"),
        ("ScaleUp", "request for availability", "Frontend Dev", "When are you available for interview?"),
        ("DataFlow", "when are you available", "Backend Dev", "Can you let us know your availability?"),
        
        # Interview variations
        ("TechGiant", "Interview invitation", "Software Architect", "Interview invitation - Software Architect"),
        ("NextGen", "interview scheduled", "QA Engineer", "Your interview has been scheduled"),
        ("CodeCraft", "invite you to interview", "Designer", "We would like to invite you to interview"),
        
        # Other statuses that should also be handled
        ("StartupHub", "Application confirmation", "Engineer", "We have received your application"),
        ("TestCorp", "Assessment sent", "Developer", "Please complete this assessment"),
        ("ExampleInc", "Information request", "Analyst", "We need additional portfolio samples"),
        
        # Edge cases
        ("EdgeCase1", "no response", "Mystery Role", "No response received"),
        ("EdgeCase2", "Unknown status", "Test Position", "This should be unmatched"),
    ]
    
    emails = []
    base_date = datetime.now() - timedelta(days=30)
    
    for i, (company, status, job_title, subject) in enumerate(test_email_data):
        email = UserEmails(
            id=f"sankey_test_{i+1:03d}",
            user_id=user_id,
            company_name=company,
            application_status=status,
            received_at=base_date + timedelta(days=i),
            subject=subject,
            job_title=job_title,
            email_from=f"hiring@{company.lower().replace(' ', '')}.com"
        )
        session.add(email)
        emails.append(email)
    
    session.commit()
    return emails

def populate_sankey_test_database():
    """Main function to populate database with Sankey test data"""
    if not DEPENDENCIES_AVAILABLE:
        print("❌ Cannot populate database: missing dependencies")
        print("Install requirements with: pip install -r requirements.txt")
        return False
    
    try:
        print("🔧 Setting up Sankey diagram test database...")
        
        # Create tables
        create_db_and_tables()
        
        with Session(engine) as session:
            # Create test user
            user_id = create_test_user(session, user_email="sankeytest@example.com")
            print(f"✅ Created test user: sankeytest@example.com (ID: {user_id})")
            
            # Create test emails
            test_emails = create_sankey_test_emails(session, user_id)
            print(f"✅ Created {len(test_emails)} test emails")
            
            # Validate the data
            from tests.debug_sankey_matching import run_comprehensive_test
            print("\n🧪 Validating test data...")
            
            # Extract status data for validation
            email_data = []
            for email in test_emails:
                email_data.append({
                    "application_status": email.application_status,
                    "company_name": email.company_name,
                    "job_title": email.job_title
                })
            
            print(f"\n📊 Test Email Status Distribution:")
            status_counts = {}
            for email in email_data:
                status = email["application_status"]
                status_counts[status] = status_counts.get(status, 0) + 1
            
            for status, count in sorted(status_counts.items()):
                print(f"  - {status}: {count}")
            
            print(f"\n🎯 Ready for testing!")
            print(f"  User ID: {user_id}")
            print(f"  Login email: sankeytest@example.com")
            print(f"  Total test emails: {len(test_emails)}")
            print(f"\n📋 To test the Sankey diagram:")
            print(f"  1. Start your application")
            print(f"  2. Login with sankeytest@example.com")
            print(f"  3. Go to dashboard and download Sankey diagram")
            print(f"  4. Verify the diagram shows proper categorization")
            
            return True
            
    except Exception as e:
        print(f"❌ Error setting up test database: {e}")
        import traceback
        traceback.print_exc()
        return False

def clean_test_data(user_id: str = None):
    """Clean up test data from the database"""
    if not DEPENDENCIES_AVAILABLE:
        print("❌ Cannot clean database: missing dependencies")
        return
    
    try:
        with Session(engine) as session:
            if user_id:
                # Clean specific user
                user = session.get(Users, user_id)
                if user:
                    session.delete(user)
                
                emails = session.query(UserEmails).filter(UserEmails.user_id == user_id).all()
                for email in emails:
                    session.delete(email)
                
                session.commit()
                print(f"✅ Cleaned test data for user: {user_id}")
            else:
                # Clean all test users (those with test emails)
                test_users = session.query(Users).filter(Users.user_email.like("%test%")).all()
                for user in test_users:
                    emails = session.query(UserEmails).filter(UserEmails.user_id == user.user_id).all()
                    for email in emails:
                        session.delete(email)
                    session.delete(user)
                
                session.commit()
                print(f"✅ Cleaned {len(test_users)} test users and their emails")
                
    except Exception as e:
        print(f"❌ Error cleaning test data: {e}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Database utilities for Sankey diagram testing")
    parser.add_argument("--populate", action="store_true", help="Populate database with test data")
    parser.add_argument("--clean", action="store_true", help="Clean test data from database")
    parser.add_argument("--user-id", type=str, help="Specific user ID to clean (use with --clean)")
    
    args = parser.parse_args()
    
    if args.populate:
        success = populate_sankey_test_database()
        sys.exit(0 if success else 1)
    elif args.clean:
        clean_test_data(args.user_id)
    else:
        print("Use --populate to add test data or --clean to remove test data")
        print("Example: python db_test_utils.py --populate")
        print("Example: python db_test_utils.py --clean --user-id specific_user_id")
