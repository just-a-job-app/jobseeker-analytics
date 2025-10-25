import sys
import os
import pytest
import sqlalchemy as sa
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel
from fastapi.testclient import TestClient
from fastapi import Request
from datetime import datetime
from unittest.mock import Mock

# Add the parent directory to sys.path BEFORE any other imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import database  # noqa: E402 DONT MOVE THIS
import main  # noqa: E402
from session.session_layer import validate_session  # noqa: E402
from db.processing_tasks import STARTED, FINISHED, TaskRuns  # noqa: E402
from db.users import Users # noqa: E402

# Use SQLite for GitHub CI pipeline and Docker environments
os.environ["DATABASE_URL"] = "sqlite:///:memory:"


@pytest.fixture
def engine(monkeypatch):
    # Use SQLite for testing with threading support for FastAPI TestClient
    # StaticPool ensures all connections share the same in-memory database
    test_engine = sa.create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )

    monkeypatch.setattr(database, "engine", test_engine)

    database.create_db_and_tables()

    yield test_engine

    # Cleanup for SQLite
    for table in reversed(SQLModel.metadata.sorted_tables):
        with test_engine.begin() as transaction:
            transaction.execute(table.delete())


@pytest.fixture
def db_session(engine, monkeypatch):
    with Session(database.engine) as session:
        yield session


@pytest.fixture
def task_factory(db_session, logged_in_user):
    def _create_task(status=STARTED, processed_emails=0):
        task = TaskRuns(
            user=logged_in_user, status=status, processed_emails=processed_emails
        )
        db_session.add(task)
        db_session.commit()
        return task

    return _create_task


@pytest.fixture
def user_factory(db_session):
    def _create_user(
        user_id="123", user_email="user@example.com", start_date=datetime(2000, 1, 1)
    ):
        user = Users(user_id=user_id, user_email=user_email, start_date=start_date)
        db_session.add(user)
        db_session.commit()
        return user

    return _create_user


@pytest.fixture
def logged_in_user(user_factory):
    return user_factory()


@pytest.fixture
def started_task(task_factory):
    return task_factory(status=STARTED)


@pytest.fixture
def finished_task(task_factory):
    return task_factory(status=FINISHED)


@pytest.fixture
def task_with_300_processed_emails(task_factory):
    return task_factory(status=STARTED, processed_emails=300)


@pytest.fixture
def client_factory(db_session):
    def _make_client(user=None):
        main.app.dependency_overrides[database.request_session] = lambda: db_session
        if user:
            user_id = user.user_id
            main.app.dependency_overrides[validate_session] = lambda: user_id
        else:
            # Simulate not logged in: validate_session returns empty string
            main.app.dependency_overrides[validate_session] = lambda: ""
        return TestClient(main.app)

    return _make_client


@pytest.fixture
def logged_in_client(client_factory, logged_in_user):
    return client_factory(user=logged_in_user)


@pytest.fixture
def incognito_client(client_factory):
    return client_factory(user=None)


@pytest.fixture
def mock_request():
    return Mock(spec=Request)


@pytest.fixture
def mock_authenticated_user(logged_in_user):
    """Create a mock AuthenticatedUser that matches the database user"""
    from utils.auth_utils import AuthenticatedUser
    from unittest.mock import Mock
    from google.oauth2.credentials import Credentials

    # Create mock credentials
    mock_creds = Mock(spec=Credentials)
    mock_creds.id_token = "mock_token"
    mock_creds.client_id = "mock_client_id"

    # Create AuthenticatedUser with the same user_id and user_email as the database user
    auth_user = AuthenticatedUser(
        creds=mock_creds,
        _user_id=logged_in_user.user_id,
        _user_email=logged_in_user.user_email,
    )

    # Mock the service to avoid actual Gmail API calls
    mock_service = Mock()
    auth_user.service = mock_service

    return auth_user
