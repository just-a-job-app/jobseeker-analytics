from fastapi import APIRouter, Depends, Request, HTTPException
from db.feedback_submissions import FeedbackSubmission
from datetime import datetime
from session.session_layer import validate_session
import database
import logging
from slowapi import Limiter
from slowapi.util import get_remote_address
from pydantic import BaseModel
from typing import Optional

logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address)

router = APIRouter()

class FeedbackSubmissionModel(BaseModel):
    github_issue_id: int

@limiter.limit("6/minute")
@router.post("/feedback-submission")
def create_feedback_submission(
    submission: FeedbackSubmissionModel,
    db_session: database.DBSession,
    request: Request,
    user_id: str = Depends(validate_session),
):
    feedback = FeedbackSubmission(
        user_id=user_id,
        github_issue_id=submission.github_issue_id,
        created_at=datetime.utcnow(),
    )
    try:
        db_session.add(feedback)
        logger.info(f"Feedback submission created: {feedback}")
        db_session.commit()
        db_session.refresh(feedback)
    except Exception as e:
        logger.error(f"Failed to create feedback submission: {e}")
        raise HTTPException(status_code=500, detail="Failed to create feedback submission")
    return {"id": feedback.id} 