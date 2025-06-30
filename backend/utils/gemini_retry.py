"""
Intelligent retry logic for Gemini API rate limits
"""
import re
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


def parse_rate_limit_error(error_str: str) -> dict:
    """
    Parse Gemini API rate limit error to understand the limit type and retry time
    
    Returns:
        dict with keys:
        - limit_type: 'rpm', 'daily', or 'unknown'
        - retry_after: seconds to wait (estimated)
        - message: human-readable message
    """
    error_lower = error_str.lower()
    
    # Check for explicit retry time
    retry_match = re.search(r'retry after ([\d.]+) seconds', error_str, re.IGNORECASE)
    explicit_retry = float(retry_match.group(1)) if retry_match else None
    
    # Determine limit type
    if 'per minute' in error_lower or 'rpm' in error_lower:
        return {
            'limit_type': 'rpm',
            'retry_after': explicit_retry or 60,  # Wait 1 minute for RPM limits
            'message': 'Requests per minute limit reached. This resets every minute.'
        }
    elif 'per day' in error_lower or 'daily' in error_lower or 'resource_exhausted' in error_lower:
        # Calculate seconds until midnight UTC
        utc_now = datetime.utcnow()
        utc_midnight = (utc_now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        seconds_until_midnight = (utc_midnight - utc_now).total_seconds()
        
        return {
            'limit_type': 'daily',
            'retry_after': explicit_retry or seconds_until_midnight,
            'message': f'Daily quota exhausted. Resets at midnight UTC ({seconds_until_midnight/3600:.1f} hours)'
        }
    else:
        return {
            'limit_type': 'unknown',
            'retry_after': explicit_retry or 300,  # Default 5 minutes
            'message': 'Unknown rate limit type. Waiting before retry.'
        }


def should_retry_task(error_str: str, attempt: int, max_attempts: int = 5) -> tuple[bool, float]:
    """
    Determine if we should retry a task based on the error
    
    Returns:
        tuple of (should_retry: bool, wait_seconds: float)
    """
    limit_info = parse_rate_limit_error(error_str)
    
    # Log the parsed information
    logger.warning(
        f"Rate limit analysis:\n"
        f"  Type: {limit_info['limit_type']}\n"
        f"  Message: {limit_info['message']}\n"
        f"  Suggested wait: {limit_info['retry_after']:.0f} seconds"
    )
    
    # For daily limits, don't retry if it's more than 1 hour until reset
    if limit_info['limit_type'] == 'daily' and limit_info['retry_after'] > 3600:
        logger.error(f"Daily quota exhausted. Not retrying (would need to wait {limit_info['retry_after']/3600:.1f} hours)")
        return False, 0
    
    # For RPM limits, always retry (they reset quickly)
    if limit_info['limit_type'] == 'rpm':
        return True, limit_info['retry_after']
    
    # For unknown limits, retry with exponential backoff
    if attempt < max_attempts:
        wait_time = min(limit_info['retry_after'], 300 * (2 ** attempt))  # Cap at 5 min * 2^attempt
        return True, wait_time
    
    return False, 0


def calculate_optimal_batch_size(current_rpm: int, target_rpm: int = 10) -> int:
    """
    Calculate optimal batch size based on current and target RPM
    
    Args:
        current_rpm: Current requests per minute being made
        target_rpm: Target/allowed requests per minute
        
    Returns:
        Recommended batch size
    """
    if current_rpm <= target_rpm:
        return 1  # No batching needed
    
    # Calculate batch size to stay under limit
    batch_size = max(1, int(current_rpm / target_rpm))
    
    # Cap at reasonable maximum
    return min(batch_size, 10)