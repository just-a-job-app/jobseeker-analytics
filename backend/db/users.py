from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa

class UserData(BaseModel):
    user_id: str
    user_email: str
    start_date: datetime

class Users(SQLModel, table=True):
    __tablename__ = "users"
    user_id: str = Field(default = None, primary_key = True)
    user_email: str = Field(nullable=False)                      
    start_date: datetime = Field(nullable=True) # Start date for job applications

    # Add role field to distinguish generic users from coaches
    role: str = Field(default="jobseeker") # 'jobseeker', 'coach'

class CoachClientLink(SQLModel, table=True):
    __tablename__ = "coach_client_link"
    coach_id: str = Field(foreign_key="users.user_id", primary_key=True)
    client_id: str = Field(foreign_key="users.user_id", primary_key=True)
    start_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    # If NULL, the relationship is currently active.
    end_date: Optional[datetime] = Field(default=None, nullable=True)
    created: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated: datetime = Field(
        sa_column_kwargs={"onupdate": sa.func.now()},
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )