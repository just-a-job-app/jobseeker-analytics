"""
Optimization strategies for Gemini API usage
"""
import time
from typing import List, Dict, Any
import logging
from utils.config_utils import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class BatchProcessor:
    """Process emails in batches to reduce API calls"""
    
    def __init__(self, batch_size: int = None):
        self.batch_size = batch_size or settings.GEMINI_BATCH_SIZE
        self.batch = []
    
    def add_email(self, email: Dict[str, Any]):
        """Add email to batch"""
        self.batch.append(email)
        if len(self.batch) >= self.batch_size:
            return True  # Batch is full
        return False
    
    def get_batch_prompt(self) -> str:
        """Create a single prompt for multiple emails"""
        prompt = """Process the following emails and return a JSON array with results for each:
        
        For each email, extract:
        1. job_application_status (use the standard labels)
        2. company_name (if not false positive)
        3. job_title (if not false positive)
        
        Return format: 
        [
            {"email_id": "id1", "job_application_status": "...", "company_name": "...", "job_title": "..."},
            {"email_id": "id2", "job_application_status": "...", "company_name": "...", "job_title": "..."}
        ]
        
        Emails to process:
        """
        
        for i, email in enumerate(self.batch):
            prompt += f"\n\n--- Email {i+1} (ID: {email['id']}) ---\n{email['text_content']}\n"
        
        return prompt
    
    def clear_batch(self):
        """Clear the current batch"""
        self.batch = []


class RateLimitManager:
    """Manage rate limits more intelligently"""
    
    def __init__(self):
        self.request_times = []
        self.requests_per_minute = settings.GEMINI_REQUESTS_PER_MINUTE
        
    def can_make_request(self) -> bool:
        """Check if we can make a request without hitting rate limit"""
        now = time.time()
        # Remove requests older than 1 minute
        self.request_times = [t for t in self.request_times if now - t < 60]
        
        if len(self.request_times) < self.requests_per_minute:
            return True
        return False
    
    def record_request(self):
        """Record that a request was made"""
        self.request_times.append(time.time())
    
    def wait_time(self) -> float:
        """Calculate how long to wait before next request"""
        if self.can_make_request():
            return 0
        
        # Find the oldest request in the window
        oldest_request = min(self.request_times)
        wait_time = 60 - (time.time() - oldest_request) + 1  # +1 second buffer
        return max(0, wait_time)


# Cache for common email patterns
EMAIL_PATTERN_CACHE = {
    # Add common patterns here to avoid API calls
    "thank you for applying": {
        "job_application_status": "Application confirmation",
        "confidence": 0.9
    },
    "unfortunately": {
        "job_application_status": "Rejection",
        "confidence": 0.8
    },
    "we regret to inform": {
        "job_application_status": "Rejection",
        "confidence": 0.95
    },
    "congratulations": {
        "job_application_status": "Offer made",
        "confidence": 0.9
    },
    "interview": {
        "job_application_status": "Interview invitation",
        "confidence": 0.8
    }
}


def check_pattern_cache(email_text: str) -> Dict[str, Any] | None:
    """Check if email matches common patterns to avoid API call"""
    email_lower = email_text.lower()
    
    for pattern, result in EMAIL_PATTERN_CACHE.items():
        if pattern in email_lower and result["confidence"] > 0.85:
            logger.info(f"Pattern match found: {pattern}")
            return result
    
    return None