from fastapi import APIRouter, Depends, Request
from db.feedback_submissions import FeedbackSubmission
from datetime import datetime
from session.session_layer import validate_session
import database

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
    db_session.add(feedback)
    db_session.commit()
    db_session.refresh(feedback)
    return {"id": feedback.id} 