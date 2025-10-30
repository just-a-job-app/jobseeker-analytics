"""
This file contains the main constants used in the application.
"""

from datetime import datetime, timedelta
from pathlib import Path
from utils.filter_utils import (
    parse_base_filter_config,
)  # , parse_override_filter_config

# The list of all possible statuses that the function can return.
ALL_STATUSES = [
    "No Response",
    "Applied",
    "Interview Scheduled",
    "Request for Availability",
    "On Hold",
    "Rejection",
    "Offer Extended"
]

# A unified dictionary of all keywords and variations, sorted by length
# from longest to shortest.
# This ensures the most specific phrases are checked first.
ALL_STATUS_KEYWORDS = {
    # Rejection
    "not moving forward": "Rejection",
    "decided to move forward with": "Rejection",
    "pursue other candidates": "Rejection",
    "have decided not to": "Rejection",
    "not the right fit": "Rejection",
    "not a good match": "Rejection",
    "unfortunately": "Rejection",

    # Offer Extended
    "offer of employment": "Offer Extended",
    "we'd like to extend": "Offer Extended",
    "your official offer": "Offer Extended",
    "congratulations": "Offer Extended",
    "job offer": "Offer Extended",
    "congrats": "Offer Extended",
    "offered": "Offer Extended",

    # Interview Scheduled
    "interview scheduled": "Interview Scheduled",
    "interview date": "Interview Scheduled",
    "phone screen": "Interview Scheduled",
    "video call": "Interview Scheduled",
    "confirmed": "Interview Scheduled",
    "interview": "Interview Scheduled",

    # Request for Availability
    "your availability": "Request for Availability",
    "when are you available": "Request for Availability",
    "your schedule": "Request for Availability",
    "discuss next steps": "Request for Availability",
    "let us know what day works": "Request for Availability",
    "schedule": "Request for Availability",

    # Applied
    "application received": "Applied",
    "thank you for your interest": "Applied",
    "application submitted": "Applied",
    "received": "Applied",
    "applied": "Applied",

    # On Hold
    "on hold": "On Hold",
    "under review": "On Hold",
    "future position": "On Hold",
    "we will be in touch": "On Hold",
    "patience": "On Hold",
    "holding": "On Hold"
}

GENERIC_ATS_DOMAINS = [
    "us.greenhouse-mail.io",
    "smartrecruiters.com",
    "linkedin.com",
    "ashbyhq.com",
    "hire.lever.co",
    "hi.wellfound.com",
    "talent.icims.com",
    "myworkday.com",
    "otta.com",
]

DEFAULT_DAYS_AGO = 30
# Get the current date
current_date = datetime.now()

# Subtract 30 days
date_days_ago = current_date - timedelta(days=DEFAULT_DAYS_AGO)

# Format the date in the required format (YYYY/MM/DD)
formatted_date = date_days_ago.strftime("%Y/%m/%d")

APPLIED_FILTER_PATH = (
    Path(__file__).parent / "email_query_filters" / "applied_email_filter.yaml"
)
APPLIED_FILTER_OVERRIDES_PATH = (
    Path(__file__).parent
    / "email_query_filters"
    / "applied_email_filter_overrides.yaml"
)
QUERY_APPLIED_EMAIL_FILTER = (
    f"after:{formatted_date} -from:me -in:sent AND ({parse_base_filter_config(APPLIED_FILTER_PATH)})"
)

# ------ implement override filter later!! #
# OR \n"
# f"{parse_override_filter_config(APPLIED_FILTER_OVERRIDES_PATH)})"
# )
# label:jobs -label:query4