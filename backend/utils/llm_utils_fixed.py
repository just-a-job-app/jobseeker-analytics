import json
import logging
import os
from typing import Optional, Dict, Any
from utils.config_utils import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

# Get LLM provider from environment
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini").lower()

def process_email(email_text: str) -> Optional[Dict[str, Any]]:
    """
    Process email using the configured LLM provider.
    """
    logger.info(f"Processing email with {LLM_PROVIDER}")
    
    if LLM_PROVIDER == "gemini":
        return process_email_with_gemini(email_text)
    elif LLM_PROVIDER == "openai":
        return process_email_with_openai(email_text)
    else:
        raise ValueError(f"Unknown LLM provider: {LLM_PROVIDER}")

def process_email_with_gemini(email_text: str) -> Optional[Dict[str, Any]]:
    """Process email using Gemini API."""
    import google.generativeai as genai
    
    genai.configure(api_key=settings.GOOGLE_API_KEY)
    model = genai.GenerativeModel(settings.GEMINI_MODEL)
    
    prompt = f"""
    Categorize the following email into one of the job application status categories and extract relevant details. Only the JSON is expected in the response, not a single word more. Do NOT use backticks, do NOT use the word json.

    Job application status categories:
    - Viewed
    - Applied
    - Rejection
    - Availability request
    - Information request
    - Assessment sent
    - Interview invitation
    - Did not apply - inbound request
    - Action required from company
    - Hiring freeze notification
    - Withdrew application
    - Offer made
    - False positive

    If the status is 'False positive', only return: {{"job_application_status": "False positive"}}
    If the status is not 'False positive', return: {{"company_name": "company_name", "job_application_status": "status", "job_title": "job_title"}}

    Email: {email_text}
    """
    
    try:
        response = model.generate_content(prompt)
        response.resolve()
        response_json = response.text
        
        if response_json:
            # Clean response
            cleaned = response_json.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()
            
            logger.info(f"Gemini response: {cleaned}")
            return json.loads(cleaned)
        else:
            logger.error("Empty response from Gemini")
            return None
            
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        raise

def process_email_with_openai(email_text: str) -> Optional[Dict[str, Any]]:
    """Process email using OpenAI API."""
    try:
        # Import inside function to avoid issues
        import httpx
        from openai import OpenAI
        
        # Create a simple httpx client without proxy settings
        http_client = httpx.Client()
        
        # Initialize OpenAI client with custom http client
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            http_client=http_client
        )
        
    except Exception as e:
        logger.error(f"Failed to initialize OpenAI client: {e}")
        # Fallback to requests-based approach
        import requests
        
        headers = {
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are a job application email categorizer. Only respond with valid JSON."},
                {"role": "user", "content": f"""
                Categorize the following email into a job application status. Only respond with valid JSON.

                Job application status categories:
                - Viewed: Company viewed your application
                - Applied: Confirmation that you applied for a job
                - Rejection: Company rejected your application
                - Availability request: Company asking for your availability
                - Information request: Company asking for additional information
                - Assessment sent: Company sent you a test or assignment
                - Interview invitation: Company invited you to an interview
                - Did not apply - inbound request: Recruiter reached out to you first
                - Action required from company: Waiting for company's response
                - Hiring freeze notification: Position is on hold
                - Withdrew application: You withdrew your application
                - Offer made: Company extended a job offer
                - False positive: Not related to job applications

                If the status is 'False positive', only return: {{"job_application_status": "False positive"}}
                If the status is not 'False positive', return: {{"company_name": "company_name", "job_application_status": "status", "job_title": "job_title"}}

                Email: {email_text}
                """}
            ],
            "temperature": 0,
            "max_tokens": 200,
            "response_format": {"type": "json_object"}
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            response_text = result['choices'][0]['message']['content']
            logger.info(f"OpenAI response: {response_text}")
            return json.loads(response_text)
        else:
            raise Exception(f"OpenAI API error: {response.status_code} - {response.text}")
    
    # If client initialized successfully, use it
    prompt = f"""
    Categorize the following email into a job application status. Only respond with valid JSON.

    Job application status categories:
    - Viewed: Company viewed your application
    - Applied: Confirmation that you applied for a job
    - Rejection: Company rejected your application
    - Availability request: Company asking for your availability
    - Information request: Company asking for additional information
    - Assessment sent: Company sent you a test or assignment
    - Interview invitation: Company invited you to an interview
    - Did not apply - inbound request: Recruiter reached out to you first
    - Action required from company: Waiting for company's response
    - Hiring freeze notification: Position is on hold
    - Withdrew application: You withdrew your application
    - Offer made: Company extended a job offer
    - False positive: Not related to job applications

    If the status is 'False positive', only return: {{"job_application_status": "False positive"}}
    If the status is not 'False positive', return: {{"company_name": "company_name", "job_application_status": "status", "job_title": "job_title"}}

    Email: {email_text}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a job application email categorizer. Only respond with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=200,
            response_format={"type": "json_object"}
        )
        
        response_text = response.choices[0].message.content
        logger.info(f"OpenAI response: {response_text}")
        return json.loads(response_text)
        
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        raise