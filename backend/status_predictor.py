
from constants import ALL_STATUS_KEYWORDS

def predict_interview_status(email_data: dict) -> str:
    """
    Predicts the status of a job application email based on its content.
    """
    subject = email_data.get('subject', '')
    body = email_data.get('body', '')

    # Combine the subject and body together.
    full_text = f"{subject} {body}".lower()

    # Iterate through a single, prioritized dictionary.
    for keyword, status in ALL_STATUS_KEYWORDS.items():
        if keyword in full_text:
            return status

    # If no keywords were found, return the default status.
    return "No Response"