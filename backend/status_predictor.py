import re
from constants import STATUS_KEYWORDS

def predict_interview_status(email_data: dict) -> str:
    """
    Predicts the status of a job application email based on its content.
    """
    subject = email_data.get('subject', '')
    body = email_data.get('body', '')

    # Combine the subject and body together.
    full_text = f"{subject} {body}".lower()

    # Break the text into a list of individual words.
    words = re.split(r'\W+', full_text)

    # Create a list of all the unique words for a faster search.
    words_set = set(words)

    # Go through each keyword we're looking for to find a match.
    for keyword, status in STATUS_KEYWORDS.items():
        # Check if the keyword exists in the email's words.
        if keyword in words_set:
            return status

    # If no keywords were found, assume there is no status.
    return "No Response"