import json
import logging
import os
from typing import Optional, Dict, Any
from anthropic import Anthropic
from openai import OpenAI
import google.generativeai as genai
from google.ai.generativelanguage_v1beta2 import GenerateTextResponse
from utils.config_utils import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

# LLM provider selection
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "claude").lower()  # claude, openai, or gemini

# Initialize clients based on provider
if LLM_PROVIDER == "claude":
    anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
elif LLM_PROVIDER == "openai":
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
elif LLM_PROVIDER == "gemini":
    genai.configure(api_key=settings.GOOGLE_API_KEY)
    gemini_model = genai.GenerativeModel(settings.GEMINI_MODEL)

def process_email_with_claude(email_text: str) -> Optional[Dict[str, Any]]:
    """Process email using Claude API."""
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
        response = anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=200,
            temperature=0,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response_text = response.content[0].text
        logger.info(f"Claude response: {response_text}")
        
        # Parse JSON response
        return json.loads(response_text)
        
    except Exception as e:
        logger.error(f"Claude API error: {e}")
        raise

def process_email_with_openai(email_text: str) -> Optional[Dict[str, Any]]:
    """Process email using OpenAI API."""
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
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",  # Fast and cost-effective
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
        
        # Parse JSON response
        return json.loads(response_text)
        
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        raise

def process_email_with_gemini(email_text: str) -> Optional[Dict[str, Any]]:
    """Process email using Gemini API (original implementation)."""
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
        response: GenerateTextResponse = gemini_model.generate_content(prompt)
        response.resolve()
        response_json: str = response.text
        logger.info("Received response from model: %s", response_json)
        
        if response_json:
            # Clean response
            cleaned_response_json = response_json.strip()
            if cleaned_response_json.startswith("```json"):
                cleaned_response_json = cleaned_response_json[7:]
            if cleaned_response_json.startswith("```"):
                cleaned_response_json = cleaned_response_json[3:]
            if cleaned_response_json.endswith("```"):
                cleaned_response_json = cleaned_response_json[:-3]
            cleaned_response_json = cleaned_response_json.strip()
            cleaned_response_json = cleaned_response_json.replace("'", '"')
            
            logger.info("Cleaned response: %s", cleaned_response_json)
            return json.loads(cleaned_response_json)
        else:
            logger.error("Empty response received from the model.")
            return None
            
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        raise

def process_email(email_text: str) -> Optional[Dict[str, Any]]:
    """
    Process email using the configured LLM provider.
    """
    logger.info(f"Processing email with {LLM_PROVIDER}")
    
    if LLM_PROVIDER == "claude":
        return process_email_with_claude(email_text)
    elif LLM_PROVIDER == "openai":
        return process_email_with_openai(email_text)
    elif LLM_PROVIDER == "gemini":
        return process_email_with_gemini(email_text)
    else:
        raise ValueError(f"Unknown LLM provider: {LLM_PROVIDER}")