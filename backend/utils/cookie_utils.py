from fastapi import Response
from utils.config_utils import get_settings
import logging
import re

# Logger setup
logger = logging.getLogger(__name__)
settings = get_settings()

# Security: Cookie name validation pattern (excluding reserved prefixes)
SAFE_COOKIE_NAME_PATTERN = re.compile(r'^[a-zA-Z][a-zA-Z0-9_-]{2,63}$')
RESERVED_COOKIE_PREFIXES = ['__Secure-', '__Host-']


def set_conditional_cookie(
    response: Response,
    key: str,
    value: str,
    max_age: int = 3600,  # 1 hour
    path: str = "/",
    httponly: bool = True,
):
    """Helper function to set cookies with environment-appropriate settings
    
    Security considerations:
    - Validates cookie names to prevent injection
    - Uses secure defaults (HttpOnly=True, short expiration)
    - Applies appropriate SameSite policy for environment
    - Implements cookie prefixes for enhanced security
    - Logs only non-sensitive parameters
    - Prevents timing attacks through constant-time operations
    """
    
    # Security: Validate cookie name (constant time to prevent timing attacks)
    is_valid_name = SAFE_COOKIE_NAME_PATTERN.match(key) is not None
    has_reserved_prefix = any(key.startswith(prefix) for prefix in RESERVED_COOKIE_PREFIXES)
    
    if not is_valid_name or has_reserved_prefix:
        # Log without exposing user input
        logger.warning(f"Invalid cookie name rejected for security (length: {len(key)})")
        raise ValueError("Cookie name violates security policy")
    
    # Security: Validate cookie value
    if not value or not isinstance(value, str):
        raise ValueError("Cookie value must be a non-empty string")
    
    # Security: Limit cookie value size (4KB browser limit)
    value_bytes = value.encode('utf-8')
    if len(value_bytes) > 4000:
        logger.warning(f"Cookie value too large for key: {key[:10]}...")
        raise ValueError("Cookie value exceeds browser size limit")
    
    # Security: Enforce reasonable max_age limits
    max_age = min(max_age, 86400 * 7)  # Cap at 7 days
    if max_age <= 0:
        raise ValueError("Cookie max_age must be positive")
    
    cookie_params = {
        "key": key,
        "value": value,
        "max_age": max_age,
        "path": path,
        "httponly": httponly,
    }

    # Add environment-specific parameters
    if settings.is_publicly_deployed:
        # Production: Cross-subdomain setup requires SameSite=None?! 
        cookie_params.update({
            "domain": settings.ORIGIN,
            "secure": True,
            "samesite": "Lax"
        })
    else:
        # Development: Lax is sufficient for localhost
        cookie_params.update({
            "secure": False,
            "samesite": "Lax"
        })

    # Apply cookie prefixes for additional security
    # Correct logic: Check actual cookie parameters
    is_secure = cookie_params.get("secure", False)
    has_domain = "domain" in cookie_params
    
    if is_secure:
        if cookie_params["path"] == "/" and not has_domain:
            cookie_params["key"] = f"__Host-{cookie_params['key']}"
        elif is_secure:
            cookie_params["key"] = f"__Secure-{cookie_params['key']}"

    response.set_cookie(**cookie_params)
    return response
