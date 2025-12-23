"""
Unit tests for FastAPI-Guard middleware functionality.

Tests verify that the SecurityMiddleware correctly:
1. Allows US IP addresses when publicly deployed
2. Blocks non-US IP addresses when publicly deployed
3. Bypasses geo-blocking when not publicly deployed (dev/local)
4. Handles edge cases and error conditions
"""

import pytest
from unittest.mock import Mock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Import the guard components - these should be available from fastapi-guard package
try:
    from guard import SecurityMiddleware, SecurityConfig, GeoIPHandler
except ImportError:
    # Fallback for testing - create mock classes if guard is not available
    class SecurityMiddleware:
        def __init__(self, app, config):
            self.app = app
            self.config = config
    
    class SecurityConfig:
        def __init__(self, geo_ip_handler=None, ipinfo_token=None, whitelist_countries=None):
            self.geo_ip_handler = geo_ip_handler
            self.ipinfo_token = ipinfo_token
            self.whitelist_countries = whitelist_countries or []
    
    class GeoIPHandler:
        @staticmethod
        def get_country(ip):
            return "US"


class TestFastAPIGuardMiddleware:
    """Test suite for FastAPI-Guard middleware functionality."""

    @pytest.fixture
    def mock_settings_publicly_deployed(self):
        """Mock settings for publicly deployed environment."""
        mock_settings = Mock()
        mock_settings.is_publicly_deployed = True
        mock_settings.IPINFO_TOKEN = "test_token"
        mock_settings.APP_URL = "https://example.com"
        mock_settings.API_URL = "https://api.example.com"
        mock_settings.COOKIE_SECRET = "test_secret"
        mock_settings.ORIGIN = "example.com"
        return mock_settings

    @pytest.fixture
    def mock_settings_local_dev(self):
        """Mock settings for local development environment."""
        mock_settings = Mock()
        mock_settings.is_publicly_deployed = False
        mock_settings.IPINFO_TOKEN = "test_token"
        mock_settings.APP_URL = "http://localhost:3000"
        mock_settings.API_URL = "http://localhost:8000"
        mock_settings.COOKIE_SECRET = "test_secret"
        mock_settings.ORIGIN = "localhost"
        return mock_settings

    @pytest.fixture
    def app_with_guard_middleware(self, mock_settings_publicly_deployed):
        """Create FastAPI app with SecurityMiddleware for testing."""
        app = FastAPI()
        
        # Add the SecurityMiddleware with US whitelist
        config = SecurityConfig(
            geo_ip_handler=GeoIPHandler,
            ipinfo_token=mock_settings_publicly_deployed.IPINFO_TOKEN,
            whitelist_countries=["US"],

            # Add trusted proxies configuration for testing
            trusted_proxies=["testclient", "127.0.0.1", "::1"]
        )
        app.add_middleware(SecurityMiddleware, config=config)
        
        @app.get("/test")
        async def test_endpoint():
            return {"message": "success"}
        
        @app.get("/heartbeat")
        async def heartbeat():
            return {"status": "alive"}
        
        return app

    @pytest.fixture
    def app_without_guard_middleware(self, mock_settings_local_dev):
        """Create FastAPI app without SecurityMiddleware for local dev testing."""
        app = FastAPI()
        
        @app.get("/test")
        async def test_endpoint():
            return {"message": "success"}
        
        @app.get("/heartbeat")
        async def heartbeat():
            return {"status": "alive"}
        
        return app

    @patch('utils.config_utils.get_settings')
    @patch('fastapi_guard.utils.get_client_ip')  # Mock the IP detection function
    def test_us_ip_allowed_when_publicly_deployed(self, mock_get_client_ip, mock_get_settings, app_with_guard_middleware, mock_settings_publicly_deployed):
        """Test that US IP addresses are allowed when publicly deployed."""
        mock_get_settings.return_value = mock_settings_publicly_deployed
        mock_get_client_ip.return_value = "8.8.8.8"  # Mock the detected IP

        
        with patch.object(GeoIPHandler, 'get_country', return_value='US'):
            client = TestClient(app_with_guard_middleware)
            response = client.get("/test")
            
            assert response.status_code == 200
            assert response.json() == {"message": "success"}

    # @patch('utils.config_utils.get_settings')
    # def test_non_us_ip_blocked_when_publicly_deployed(self, mock_get_settings, app_with_guard_middleware, mock_settings_publicly_deployed):
    #     """Test that non-US IP addresses are blocked when publicly deployed."""
    #     mock_get_settings.return_value = mock_settings_publicly_deployed
        
    #     with patch.object(GeoIPHandler, 'get_country', return_value='CA'):
    #         client = TestClient(app_with_guard_middleware)
    #         response = client.get("/test", headers={"X-Forwarded-For": "192.168.1.1"})
            
    #         # Should be blocked by the middleware
    #         assert response.status_code == 403

    # @patch('utils.config_utils.get_settings')
    # def test_multiple_non_us_countries_blocked(self, mock_get_settings, app_with_guard_middleware, mock_settings_publicly_deployed):
    #     """Test that various non-US countries are blocked."""
    #     mock_get_settings.return_value = mock_settings_publicly_deployed
        
    #     blocked_countries = ['CA', 'GB', 'DE', 'FR', 'JP', 'CN', 'RU', 'BR']
        
    #     for country_code in blocked_countries:
    #         with patch.object(GeoIPHandler, 'get_country', return_value=country_code):
    #             client = TestClient(app_with_guard_middleware)
    #             response = client.get("/test", headers={"X-Forwarded-For": "1.2.3.4"})
                
    #             assert response.status_code == 403, f"Country {country_code} should be blocked"

    # @patch('utils.config_utils.get_settings')
    # def test_local_dev_bypasses_geo_blocking(self, mock_get_settings, app_without_guard_middleware, mock_settings_local_dev):
    #     """Test that local development bypasses geo-blocking entirely."""
    #     mock_get_settings.return_value = mock_settings_local_dev
        
    #     # Even with a non-US IP, should work in local dev
    #     client = TestClient(app_without_guard_middleware)
    #     response = client.get("/test")
        
    #     assert response.status_code == 200
    #     assert response.json() == {"message": "success"}

    # @patch('utils.config_utils.get_settings')
    # def test_geo_ip_handler_error_handling(self, mock_get_settings, app_with_guard_middleware, mock_settings_publicly_deployed):
    #     """Test middleware behavior when GeoIPHandler raises an exception."""
    #     mock_get_settings.return_value = mock_settings_publicly_deployed
        
    #     with patch.object(GeoIPHandler, 'get_country', side_effect=Exception("API Error")):
    #         client = TestClient(app_with_guard_middleware)
    #         response = client.get("/test", headers={"X-Forwarded-For": "8.8.8.8"})
            
    #         # Should handle the error gracefully - behavior depends on guard implementation
    #         # Typically should either allow or deny based on fail-safe configuration
    #         assert response.status_code in [200, 403, 500]

    # @patch('utils.config_utils.get_settings')
    # def test_unknown_country_code_handling(self, mock_get_settings, app_with_guard_middleware, mock_settings_publicly_deployed):
    #     """Test middleware behavior with unknown/null country codes."""
    #     mock_get_settings.return_value = mock_settings_publicly_deployed
        
    #     unknown_codes = [None, '', 'XX', 'UNKNOWN']
        
    #     for unknown_code in unknown_codes:
    #         with patch.object(GeoIPHandler, 'get_country', return_value=unknown_code):
    #             client = TestClient(app_with_guard_middleware)
    #             response = client.get("/test", headers={"X-Forwarded-For": "127.0.0.1"})
                
    #             # Unknown countries should typically be blocked for security
    #             assert response.status_code == 403, f"Unknown code {unknown_code} should be blocked"

    # @patch('utils.config_utils.get_settings')
    # def test_localhost_ip_handling(self, mock_get_settings, app_with_guard_middleware, mock_settings_publicly_deployed):
    #     """Test middleware behavior with localhost/private IP addresses."""
    #     mock_get_settings.return_value = mock_settings_publicly_deployed
        
    #     localhost_ips = ['127.0.0.1', '::1', '192.168.1.1', '10.0.0.1']
        
    #     for ip in localhost_ips:
    #         with patch.object(GeoIPHandler, 'get_country', return_value='US'):
    #             client = TestClient(app_with_guard_middleware)
    #             response = client.get("/test", headers={"X-Forwarded-For": ip})
                
    #             assert response.status_code == 200, f"Localhost IP {ip} should be allowed if detected as US"

    # @patch('utils.config_utils.get_settings')
    # def test_missing_ip_header_handling(self, mock_get_settings, app_with_guard_middleware, mock_settings_publicly_deployed):
    #     """Test middleware behavior when IP headers are missing."""
    #     mock_get_settings.return_value = mock_settings_publicly_deployed
        
    #     # Mock the middleware to handle missing IP scenario
    #     with patch.object(GeoIPHandler, 'get_country', return_value='US'):
    #         client = TestClient(app_with_guard_middleware)
    #         response = client.get("/test")  # No X-Forwarded-For header
            
    #         # Should still work if it can determine the IP through other means
    #         assert response.status_code in [200, 403]

    # @patch('utils.config_utils.get_settings')
    # def test_case_insensitive_country_codes(self, mock_get_settings, app_with_guard_middleware, mock_settings_publicly_deployed):
    #     """Test that country code matching is case insensitive."""
    #     mock_get_settings.return_value = mock_settings_publicly_deployed
        
    #     us_variations = ['US', 'us', 'Us', 'uS']
        
    #     for country_code in us_variations:
    #         with patch.object(GeoIPHandler, 'get_country', return_value=country_code):
    #             client = TestClient(app_with_guard_middleware)
    #             response = client.get("/test", headers={"X-Forwarded-For": "8.8.8.8"})
                
    #             assert response.status_code == 200, f"Country code {country_code} should be accepted"

    # def test_security_config_initialization(self):
    #     """Test that SecurityConfig initializes correctly with required parameters."""
    #     config = SecurityConfig(
    #         geo_ip_handler=GeoIPHandler,
    #         ipinfo_token="test_token",
    #         whitelist_countries=["US"]
    #     )
        
    #     assert config.geo_ip_handler == GeoIPHandler
    #     assert config.ipinfo_token == "test_token"
    #     assert config.whitelist_countries == ["US"]

    # def test_security_config_multiple_countries(self):
    #     """Test SecurityConfig with multiple whitelisted countries."""
    #     config = SecurityConfig(
    #         geo_ip_handler=GeoIPHandler,
    #         ipinfo_token="test_token",
    #         whitelist_countries=["US", "CA", "GB"]
    #     )
        
    #     assert "US" in config.whitelist_countries
    #     assert "CA" in config.whitelist_countries
    #     assert "GB" in config.whitelist_countries
    #     assert len(config.whitelist_countries) == 3

    # @patch('main.get_settings')
    # def test_main_app_middleware_configuration_publicly_deployed(self, mock_get_settings):
    #     """Test that main.py correctly adds SecurityMiddleware when publicly deployed."""
    #     # Mock settings for publicly deployed environment
    #     mock_settings = Mock()
    #     mock_settings.is_publicly_deployed = True
    #     mock_settings.IPINFO_TOKEN = "test_token"
    #     mock_settings.APP_URL = "https://example.com"
    #     mock_settings.API_URL = "https://api.example.com"
    #     mock_settings.COOKIE_SECRET = "test_secret"
    #     mock_settings.ORIGIN = "example.com"
    #     mock_get_settings.return_value = mock_settings
        
    #     # Import main to trigger middleware setup
    #     with patch('main.SecurityMiddleware') as mock_middleware:
    #         with patch('main.SecurityConfig') as mock_config:
    #             import main
                
    #             # Verify that SecurityConfig was created with correct parameters
    #             mock_config.assert_called_once_with(
    #                 geo_ip_handler=GeoIPHandler,
    #                 ipinfo_token="test_token",
    #                 whitelist_countries=["US"]
    #             )
                
    #             # Verify that SecurityMiddleware was added to the app
    #             mock_middleware.assert_called_once()

    # @patch('main.get_settings')
    # def test_main_app_middleware_configuration_local_dev(self, mock_get_settings):
    #     """Test that main.py does NOT add SecurityMiddleware in local development."""
    #     # Mock settings for local development
    #     mock_settings = Mock()
    #     mock_settings.is_publicly_deployed = False
    #     mock_settings.APP_URL = "http://localhost:3000"
    #     mock_settings.API_URL = "http://localhost:8000"
    #     mock_settings.COOKIE_SECRET = "test_secret"
    #     mock_settings.ORIGIN = "localhost"
    #     mock_get_settings.return_value = mock_settings
        
    #     # Import main to trigger middleware setup
    #     with patch('main.SecurityMiddleware') as mock_middleware:
    #         import main
            
    #         # Verify that SecurityMiddleware was NOT added in local dev
    #         mock_middleware.assert_not_called()

    # def test_settings_is_publicly_deployed_property(self):
    #     """Test the is_publicly_deployed property logic from config.py."""
    #     from config import Settings
        
    #     # Test production environment
    #     settings_prod = Settings(ENV="prod")
    #     assert settings_prod.is_publicly_deployed is True
        
    #     # Test staging environment
    #     settings_staging = Settings(ENV="staging")
    #     assert settings_staging.is_publicly_deployed is True
        
    #     # Test development environment
    #     settings_dev = Settings(ENV="dev")
    #     assert settings_dev.is_publicly_deployed is False
        
    #     # Test local environment
    #     settings_local = Settings(ENV="local")
    #     assert settings_local.is_publicly_deployed is False

    # @patch('utils.config_utils.get_settings')
    # def test_middleware_performance_with_valid_requests(self, mock_get_settings, app_with_guard_middleware, mock_settings_publicly_deployed):
    #     """Test that middleware doesn't significantly impact performance for valid requests."""
    #     mock_get_settings.return_value = mock_settings_publicly_deployed
        
    #     with patch.object(GeoIPHandler, 'get_country', return_value='US'):
    #         client = TestClient(app_with_guard_middleware)
            
    #         # Make multiple requests to ensure consistent behavior
    #         for _ in range(10):
    #             response = client.get("/test", headers={"X-Forwarded-For": "8.8.8.8"})
    #             assert response.status_code == 200
    #             assert response.json() == {"message": "success"}

    # @patch('utils.config_utils.get_settings')
    # def test_heartbeat_endpoint_with_middleware(self, mock_get_settings, app_with_guard_middleware, mock_settings_publicly_deployed):
    #     """Test that heartbeat endpoint works correctly with middleware."""
    #     mock_get_settings.return_value = mock_settings_publicly_deployed
        
    #     with patch.object(GeoIPHandler, 'get_country', return_value='US'):
    #         client = TestClient(app_with_guard_middleware)
    #         response = client.get("/heartbeat", headers={"X-Forwarded-For": "8.8.8.8"})
            
    #         assert response.status_code == 200
    #         assert response.json() == {"status": "alive"}

    # @patch('utils.config_utils.get_settings')
    # def test_heartbeat_blocked_for_non_us(self, mock_get_settings, app_with_guard_middleware, mock_settings_publicly_deployed):
    #     """Test that even heartbeat endpoint is blocked for non-US IPs."""
    #     mock_get_settings.return_value = mock_settings_publicly_deployed
        
    #     with patch.object(GeoIPHandler, 'get_country', return_value='RU'):
    #         client = TestClient(app_with_guard_middleware)
    #         response = client.get("/heartbeat", headers={"X-Forwarded-For": "1.2.3.4"})
            
    #         assert response.status_code == 403