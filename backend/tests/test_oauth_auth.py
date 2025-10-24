from unittest.mock import Mock, patch
from utils.auth_utils import get_google_authorization_url


def test_new_user_gets_consent_prompt():
    """New users get consent screen to ensure refresh token."""
    mock_flow = Mock()
    mock_flow.authorization_url.return_value = ("https://google.com/auth", "state")
    
    get_google_authorization_url(mock_flow, has_valid_creds=False)
    
    mock_flow.authorization_url.assert_called_once_with(
        access_type='offline',
        prompt='consent'
    )


def test_returning_user_gets_select_account():
    """Returning users get account picker for smooth login."""
    mock_flow = Mock()
    mock_flow.authorization_url.return_value = ("https://google.com/auth", "state")
    
    get_google_authorization_url(mock_flow, has_valid_creds=True)
    
    mock_flow.authorization_url.assert_called_once_with(
        access_type='offline',
        prompt='select_account'
    )


def test_oauth_flow_parameters():
    """OAuth flow uses correct parameters for different user types."""
    # Test that the utility function works with different parameters
    mock_flow = Mock()
    mock_flow.authorization_url.return_value = ("https://google.com/oauth", "state")
    
    # Test new user flow
    get_google_authorization_url(mock_flow, has_valid_creds=False)
    mock_flow.authorization_url.assert_called_with(
        access_type='offline',
        prompt='consent'
    )
    
    # Reset and test returning user flow
    mock_flow.authorization_url.reset_mock()
    get_google_authorization_url(mock_flow, has_valid_creds=True)
    mock_flow.authorization_url.assert_called_with(
        access_type='offline',
        prompt='select_account'
    )
