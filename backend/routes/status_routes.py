from fastapi import APIRouter
from pydantic import BaseModel
from status_predictor import predict_interview_status

router = APIRouter()

class Email(BaseModel):
    subject: str
    body: str

@router.post("/predict_status")
def predict_status_endpoint(email_data: Email):
    """
    Predicts the interview status of an email.
    """
    email_data = email_data.dict()
    status = predict_interview_status(email_data)
    return {"status": status}