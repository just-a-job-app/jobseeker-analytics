from fastapi import APIRouter, Depends, Request, HTTPException
from db.feedback_submissions import FeedbackSubmission
from datetime import datetime
from session.session_layer import validate_session
import database
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/api/feedback-submission")
def create_feedback_submission(
    request: Request,
    github_issue_id: int,
    db_session: database.DBSession,
    user_id: str = Depends(validate_session),
):
    feedback = FeedbackSubmission(
        user_id=user_id,
        github_issue_id=github_issue_id,
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