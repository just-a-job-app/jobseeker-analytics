"""
Mock Gmail Service for demo mode and development.
Mimics the real Google Gmail API but uses test data instead.
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from tests.test_email_data import get_demo_emails, get_all_test_emails
from db.utils.test_email_utils import get_user_test_emails
import database
from sqlmodel import Session

logger = logging.getLogger(__name__)

class MockGmailService:
    """Mock Gmail service that mimics the real Google Gmail API."""
    
    def __init__(self, user_id: str = None):
        self.user_id = user_id
        self.demo_emails = get_demo_emails()
        self.all_test_emails = get_all_test_emails()
    
    def users(self):
        """Mock users() method to mimic Gmail API structure."""
        return MockUsersService(self.user_id)
    
    def get_user_test_emails(self) -> List[Dict[str, Any]]:
        """Get test emails for the current user from database."""
        if not self.user_id:
            return self.demo_emails
        
        try:
            with Session(database.engine) as db_session:
                test_emails = get_user_test_emails(self.user_id, include_demo=True)
                return [self._convert_test_email_to_gmail_format(email) for email in test_emails]
        except Exception as e:
            logger.error(f"Error getting user test emails: {e}")
            return self.demo_emails
    
    def _convert_test_email_to_gmail_format(self, test_email) -> Dict[str, Any]:
        """Convert TestEmail model to Gmail API format."""
        return {
            "id": test_email.id,
            "threadId": f"thread_{test_email.id}",
            "labelIds": ["INBOX", "UNREAD"],
            "snippet": test_email.subject[:100] + "..." if len(test_email.subject) > 100 else test_email.subject,
            "internalDate": str(int(test_email.received_at.timestamp() * 1000)),
            "payload": {
                "headers": [
                    {"name": "From", "value": test_email.email_from},
                    {"name": "To", "value": "user@example.com"},
                    {"name": "Subject", "value": test_email.subject},
                    {"name": "Date", "value": test_email.received_at.strftime("%a, %d %b %Y %H:%M:%S %z")},
                ],
                "body": {
                    "data": test_email.email_body,
                    "size": len(test_email.email_body)
                },
                "parts": []
            },
            "sizeEstimate": len(test_email.email_body),
            "historyId": "12345"
        }

class MockUsersService:
    """Mock users service to mimic Gmail API structure."""
    
    def __init__(self, user_id: str = None):
        self.user_id = user_id
        self.mock_service = MockGmailService(user_id)
    
    def messages(self):
        """Mock messages() method."""
        return MockMessagesService(self.user_id, self.mock_service)
    
    def getProfile(self):
        """Mock getProfile() method."""
        return {
            "emailAddress": "demo@example.com",
            "messagesTotal": len(self.mock_service.get_user_test_emails()),
            "threadsTotal": len(self.mock_service.get_user_test_emails()),
            "historyId": "12345"
        }

class MockMessagesService:
    """Mock messages service to mimic Gmail API structure."""
    
    def __init__(self, user_id: str, mock_service: MockGmailService):
        self.user_id = user_id
        self.mock_service = mock_service
    
    def list(self, userId: str = "me", q: str = None, maxResults: int = 100, **kwargs):
        """Mock list() method to get messages."""
        return MockListRequest(self.user_id, self.mock_service, q, maxResults)
    
    def get(self, userId: str = "me", id: str = None, format: str = "full", **kwargs):
        """Mock get() method to get a specific message."""
        return MockGetRequest(self.user_id, self.mock_service, id, format)

class MockListRequest:
    """Mock list request to mimic Gmail API response."""
    
    def __init__(self, user_id: str, mock_service: MockGmailService, query: str = None, max_results: int = 100):
        self.user_id = user_id
        self.mock_service = mock_service
        self.query = query
        self.max_results = max_results
    
    def execute(self) -> Dict[str, Any]:
        """Execute the list request and return mock data."""
        emails = self.mock_service.get_user_test_emails()
        
        # Filter by query if provided
        if self.query:
            filtered_emails = []
            query_lower = self.query.lower()
            for email in emails:
                if (query_lower in email.get("subject", "").lower() or
                    query_lower in email.get("email_from", "").lower() or
                    query_lower in email.get("company_name", "").lower()):
                    filtered_emails.append(email)
            emails = filtered_emails
        
        # Limit results
        emails = emails[:self.max_results]
        
        return {
            "messages": [{"id": email["id"]} for email in emails],
            "nextPageToken": None if len(emails) < self.max_results else "next_page_token",
            "resultSizeEstimate": len(emails)
        }

class MockGetRequest:
    """Mock get request to mimic Gmail API response."""
    
    def __init__(self, user_id: str, mock_service: MockGmailService, message_id: str = None, format: str = "full"):
        self.user_id = user_id
        self.mock_service = mock_service
        self.message_id = message_id
        self.format = format
    
    def execute(self) -> Dict[str, Any]:
        """Execute the get request and return mock data."""
        emails = self.mock_service.get_user_test_emails()
        
        # Find the specific email
        target_email = None
        for email in emails:
            if email["id"] == self.message_id:
                target_email = email
                break
        
        if not target_email:
            # Return a default email if not found
            target_email = emails[0] if emails else {
                "id": self.message_id,
                "subject": "Test Email",
                "email_from": "test@example.com",
                "email_body": "This is a test email body.",
                "received_at": datetime.now(timezone.utc)
            }
        
        if self.format == "raw":
            # Return raw format (base64 encoded)
            import base64
            raw_content = f"""From: {target_email.get('email_from', 'test@example.com')}
To: user@example.com
Subject: {target_email.get('subject', 'Test Subject')}
Date: {target_email.get('received_at', datetime.now(timezone.utc)).strftime('%a, %d %b %Y %H:%M:%S %z')}

{target_email.get('email_body', 'Test email body')}"""
            
            return {
                "id": target_email["id"],
                "threadId": f"thread_{target_email['id']}",
                "labelIds": ["INBOX"],
                "snippet": target_email.get("subject", "")[:100],
                "historyId": "12345",
                "internalDate": str(int(target_email.get("received_at", datetime.now(timezone.utc)).timestamp() * 1000)),
                "raw": base64.urlsafe_b64encode(raw_content.encode()).decode()
            }
        else:
            # Return full format
            return {
                "id": target_email["id"],
                "threadId": f"thread_{target_email['id']}",
                "labelIds": ["INBOX"],
                "snippet": target_email.get("subject", "")[:100],
                "historyId": "12345",
                "internalDate": str(int(target_email.get("received_at", datetime.now(timezone.utc)).timestamp() * 1000)),
                "payload": {
                    "headers": [
                        {"name": "From", "value": target_email.get("email_from", "test@example.com")},
                        {"name": "To", "value": "user@example.com"},
                        {"name": "Subject", "value": target_email.get("subject", "Test Subject")},
                        {"name": "Date", "value": target_email.get("received_at", datetime.now(timezone.utc)).strftime("%a, %d %b %Y %H:%M:%S %z")},
                    ],
                    "body": {
                        "data": target_email.get("email_body", "Test email body"),
                        "size": len(target_email.get("email_body", "Test email body"))
                    },
                    "parts": []
                },
                "sizeEstimate": len(target_email.get("email_body", "Test email body"))
            }

def create_mock_gmail_service(user_id: str = None) -> MockGmailService:
    """Factory function to create a mock Gmail service."""
    return MockGmailService(user_id) 