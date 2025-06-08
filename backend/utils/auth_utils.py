import logging
import uuid

from utils.file_utils import get_user_filepath

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google.oauth2 import id_token

from utils.config_utils import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()


class AuthenticatedUser:
    """
    The AuthenticatedUser class is used to
    store information about the user. This
    class is instantiated after the user has
    successfully authenticated with Google.
    """

    def __init__(self, creds: Credentials, start_date=None):
        self.creds = creds
        self.user_id, self.user_email = self.get_user_id_and_email()
        self.filepath = get_user_filepath(self.user_id)
        self.start_date = start_date

    def get_user_id_and_email(self) -> tuple:
        """
        Retrieves the user ID and email from Google OAuth2 credentials.

        Parameters:

        Returns:
        - user_id: The unique user ID.
        - email: The user's email address.
        """
        try:
            logger.info("Verifying ID token...")

            # Ensure we have an ID token
            if not self.creds.id_token:
                logger.warning("ID token is missing, trying to refresh credentials...")
                self.creds.refresh(Request())  # Refresh credentials

            # If still missing, raise an error
            if not self.creds.id_token:
                raise ValueError("No ID token available after refresh.")
    
            decoded_token = id_token.verify_oauth2_token(
                self.creds.id_token, Request(), audience=settings.GOOGLE_CLIENT_ID
            )
            user_id = decoded_token["sub"]  # 'sub' is the unique user ID
            user_email = decoded_token.get("email")  # 'email' is the user's email address
            return user_id, user_email
        
        except (KeyError, TypeError):
            self.creds = self.creds.refresh(Request())
            if not self.creds.id_token:
                proxy_user_id = str(uuid.uuid4())
                logger.error(
                    "Could not retrieve user ID. Using proxy ID: %s", proxy_user_id
                )
                return proxy_user_id, None  # Generate a random ID and return None for email
            if not hasattr(self, "_retry"):
                self._retry = True
                return self.get_user_id_and_email()
            else:
                proxy_user_id = str(uuid.uuid4())
                logger.error(
                    "Could not retrieve user ID after retry. Using proxy ID: %s",
                    proxy_user_id,
                )
                return proxy_user_id, None  # Generate a random ID and return None for email
        except Exception as e:
            logger.error("Error verifying ID token: %s", e)
            proxy_user_id = str(uuid.uuid4())
            logger.error("Could not verify ID token. Using proxy ID: %s", proxy_user_id)
            return proxy_user_id, None  # Generate a random ID and return None for email
