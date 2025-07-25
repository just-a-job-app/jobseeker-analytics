from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class TestEmails(SQLModel, table=True):
    __tablename__ = "test_emails"
    
    id: str = Field(primary_key=True)  # Unique test email ID
    user_id: str = Field(primary_key=True)  # User who owns this test email
    company_name: str
    application_status: str
    received_at: datetime
    subject: str
    job_title: str
    email_from: str
    email_body: str  # Full email body content
    is_demo_email: bool = Field(default=False)  # Flag for demo mode emails
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    # Optional fields for categorization
    category: Optional[str] = Field(default=None)  # For organizing test emails
    tags: Optional[str] = Field(default=None)  # JSON string of tags
    notes: Optional[str] = Field(default=None)  # User notes about this test email 