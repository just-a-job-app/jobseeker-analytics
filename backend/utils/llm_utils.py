import google.generativeai as genai
import time
import json
from google.ai.generativelanguage_v1beta2 import GenerateTextResponse
import logging

from utils.config_utils import get_settings

settings = get_settings()

# Configure Google Gemini API
genai.configure(api_key=settings.GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash-lite")
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

def process_email(email_text):
    prompt = f"""
        First, extract the job application status from the following email using the labels below. 
        If the status is 'False positive', only return the status as 'False positive' and do not extract company name or job title. 
        If the status is not 'False positive', then extract the company name and job title as well.
        
        Assign one of the following labels to job application status based on the main purpose or outcome of the message:
        
        Application confirmation
        Rejection
        Availability request
        Information request
        Assessment sent
        Interview invitation
        Did not apply - inbound request
        Action required from company
        Hiring freeze notification
        Withdrew application
        Offer made
        False positive

        Labeling Rules and Explanations for Job Application Status:

        Application confirmation
        Assign this label if the email confirms receipt of a job application.
        Examples: "We have received your application", "Thank you for applying", "Your application has been submitted".

        Rejection
        Use this label for emails explicitly stating that the candidate is not moving forward in the process.
        Examples: "We regret to inform you...", "We will not be proceeding with your application", "You have not been selected".

        Availability request
        Assign this label if the company asks for your availability for a call, interview, or meeting.
        Examples: "Please let us know your availability", "When are you free for a call?", "Can you share your available times?"

        Information request
        Use this label if the company requests additional information, documents, or clarification.
        Examples: "Please send your portfolio", "Can you provide references?", "We need more information about..."

        Assessment sent
        Assign this label if the company sends a test, assignment, or assessment for you to complete as part of the hiring process.
        Examples: "Please complete the attached assessment", "Here is your coding challenge", "Take-home assignment enclosed".

        Interview invitation
        Use this label if the company invites you to an interview (phone, video, or onsite).
        Examples: "We would like to invite you to interview", "Interview scheduled", "Please join us for an interview".

        Did not apply - inbound request
        Assign this label if the company or recruiter reaches out to you first about a job or recruiting opportunity, and you did not apply for the position.
        Examples: "We found your profile and would like to connect about a job", "Are you interested in this job opportunity?", "We came across your resume for a position".
        Do NOT use this label for event invitations, newsletters, or marketing emails.

        Action required from company
        Use this label if the next step is pending from the company, and you are waiting for their response or action.
        Examples: "We will get back to you", "Awaiting feedback from the team", "We will contact you with next steps".

        Hiring freeze notification
        Assign this label if the company notifies you that the position is on hold or canceled due to a hiring freeze.
        Examples: "Position is on hold", "Hiring freeze in effect", "We are pausing recruitment".

        Withdrew application
        Use this label if you (the candidate) have withdrawn your application, or the email confirms your withdrawal.
        Examples: "You have withdrawn your application", "Thank you for letting us know you are no longer interested".

        Offer made
        Assign this label if the company extends a job offer to you.
        Examples: "We are pleased to offer you the position", "Offer letter attached", "Congratulations, you have been selected".

        False positive
        Use this label if the email is not related to job applications, recruitment, or hiring.
        Examples: Newsletters, event invitations, conference invites, marketing emails, spam, unrelated notifications, or personal emails.
        Example: "Join us for our annual conference" → False positive
        Example: "Sign up for our upcoming event" → False positive

        If the status is 'False positive', only return: {{"job_application_status": "False positive"}}
        If the status is not 'False positive', return: {{"company_name": "company_name", "job_application_status": "status", "job_title": "job_title"}}
        Remove backticks. Only use double quotes. Enclose key and value pairs in a single pair of curly braces.
        Email: {email_text}
    """

    retries = 3  # Max retries
    delay = 60  # Initial delay
    for attempt in range(retries):
        try:
            logger.info("Calling generate_content")
            response: GenerateTextResponse = model.generate_content(prompt)
            response.resolve()
            response_json: str = response.text
            logger.info("Received response from model: %s", response_json)
            if response_json:
                cleaned_response_json = (
                    response_json.replace("json", "")
                    .replace("`", "")
                    .replace("'", '"')
                    .strip()
                )
                cleaned_response_json = (
                    response_json.replace("json", "")
                    .replace("`", "")
                    .replace("'", '"')
                    .strip()
                )
                logger.info("Cleaned response: %s", cleaned_response_json)
                return json.loads(cleaned_response_json)
            else:
                logger.error("Empty response received from the model.")
                return None
        except Exception as e:
            if "429" in str(e):
                logger.warning(
                    f"Rate limit hit. Retrying in {delay} seconds (attempt {attempt + 1})."
                )
                time.sleep(delay)
            else:
                logger.error(f"process_email exception: {e}")
                return None
    logger.error(f"Failed to process email after {retries} attempts.")
    return None

