"""
This file contains the main constants used in the application.
"""
from pathlib import Path
from utils.filter_utils import (
    parse_base_filter_config,
)
from constants import QUERY_APPLIED_EMAIL_FILTER

APPLIED_FILTER_PATH = (
    Path(__file__).parent.parent / "email_query_filters" / "applied_email_filter.yaml"
)

def get_start_date_email_filter(start_date: str) -> str:
    if not start_date:
        return QUERY_APPLIED_EMAIL_FILTER

    START_DATE_EMAIL_FILTER = (
        f"after:{start_date} AND ({parse_base_filter_config(APPLIED_FILTER_PATH)})"
    )
    return START_DATE_EMAIL_FILTER