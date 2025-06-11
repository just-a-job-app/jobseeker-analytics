from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class FeedbackSubmission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[str] = Field(default=None, index=True)
    github_issue_id: int = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow) 