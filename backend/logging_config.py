import logging
import sys
from typing import Dict, Any

def get_logging_config() -> Dict[str, Any]:
    """Get custom logging configuration that excludes IP addresses in development mode."""
    from config import settings
    
    # In development mode, completely disable uvicorn.access logger
    if settings.ENV == "dev":
        uvicorn_access_config = {
            "handlers": [],
            "level": "CRITICAL",  # Set to CRITICAL to effectively disable it
            "propagate": False,
        }
    else:
        # In production, enable uvicorn.access logger with standard format
        uvicorn_access_config = {
            "handlers": ["access"],
            "level": "INFO",
            "propagate": False,
        }
    
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(levelname)s - %(name)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "access": {
                "format": "%(levelname)s - %(name)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
            },
            "access": {
                "formatter": "access",
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
            },
        },
        "loggers": {
            "uvicorn": {
                "handlers": ["default"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn.error": {
                "handlers": ["default"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn.access": uvicorn_access_config,
            "fastapi": {
                "handlers": ["default"],
                "level": "INFO",
                "propagate": False,
            },
        },
        "root": {
            "handlers": ["default"],
            "level": "INFO",
        },
    } 