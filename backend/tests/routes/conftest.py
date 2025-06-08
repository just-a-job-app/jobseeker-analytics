from datetime import datetime, timedelta
from unittest import mock

import pytest
from fastapi.testclient import TestClient

from db.users import Users
import database
import main


@pytest.fixture
def client(db_session):
    main.app.dependency_overrides[database.request_session] = lambda: db_session
    test_client = TestClient(main.app)

    return test_client


@pytest.fixture
def logged_in_user(db_session, client):
    # create user
    user = Users(
        user_id="123",
        user_email="user@example.com",
        start_date=datetime(2000, 1, 1),
    )
    db_session.add(user)
    db_session.flush()

    # log in
    mock_credentials = mock.Mock(
        **{
            "expiry": datetime.utcnow() + timedelta(seconds=10),
            "token": "fake access token",
            "to_json.return_value": {"foo": "bar"},
        }
    )
    mock_decoded_token = {"sub": user.user_id, "email": user.user_email}
    with (
        mock.patch(
            "routes.auth_routes.Flow",
            **{"from_client_secrets_file.return_value.credentials": mock_credentials},
        ),
        mock.patch(
            "utils.auth_utils.id_token",
            **{"verify_oauth2_token.return_value": mock_decoded_token},
        ),
    ):
        auth_resp = client.get("/login", params={"code": "abc"}, follow_redirects=False)
        assert auth_resp.status_code == 303
        assert auth_resp.headers["Location"] == "http://localhost:3000/dashboard"

    return user
