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
from testcontainers.postgres import PostgresContainer

# Add the parent directory to sys.path BEFORE any other imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import database  # noqa: E402 DONT MOVE THIS
import main  # noqa: E402
from session.session_layer import validate_session  # noqa: E402
from db.processing_tasks import STARTED, FINISHED, TaskRuns  # noqa: E402
from db.users import Users, CoachClientLink  # noqa: E402

# Use SQLite for GitHub CI pipeline and Docker environments
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

# Force SQLite mode - set this to True to always use SQLite instead of testcontainers
FORCE_SQLITE = os.environ.get("FORCE_SQLITE", "true").lower() == "true"

# Check if running in Docker container (consistent with database.py)
IS_DOCKER_CONTAINER = bool(int(os.environ.get("IS_DOCKER_CONTAINER", 0)))


@pytest.fixture(scope="session")
def postgres_container():
    # Only use testcontainers if not running in Docker and not forced to use SQLite
    if not FORCE_SQLITE and not IS_DOCKER_CONTAINER:
        try:
            with PostgresContainer("postgres:13") as postgres:
                yield postgres
        except Exception as e:
            # If testcontainers fails, fall back to None
            print(f"Testcontainers failed: {e}. Falling back to SQLite.")
            yield None
    else:
        # Skip testcontainers when running in Docker or when forced to use SQLite
        yield None


@pytest.fixture
def engine(monkeypatch, postgres_container):
    if (
        postgres_container is not None
        and not FORCE_SQLITE
        and not IS_DOCKER_CONTAINER
    ):
        # Use PostgreSQL with testcontainers when running locally
        test_url = sa.URL.create(
            "postgresql",
            username=postgres_container.username,
            password=postgres_container.password,
            host=postgres_container.get_container_host_ip(),
            port=postgres_container.get_exposed_port(postgres_container.port),
            database=postgres_container.dbname,
        )
        test_engine = sa.create_engine(test_url)
        print("Using PostgreSQL testcontainer for tests")
    else:
        # Use SQLite when running in Docker, CI, or when forced
        test_engine = sa.create_engine(
            "sqlite:///:memory:",
            poolclass=StaticPool,
            connect_args={"check_same_thread": False},
        )
        print("Using SQLite in-memory database for tests")

    monkeypatch.setattr(database, "engine", test_engine)
    database.create_db_and_tables()

    yield test_engine

    # Clean up all tables after each test
    with test_engine.begin() as transaction:
        if (
            postgres_container is not None
            and not FORCE_SQLITE
            and not IS_DOCKER_CONTAINER
        ):
            # For PostgreSQL, use TRUNCATE for faster cleanup
            for table in reversed(SQLModel.metadata.sorted_tables):
                try:
                    transaction.execute(
                        sa.text(f"TRUNCATE TABLE {table.name} RESTART IDENTITY CASCADE")
                    )
                except Exception as e:
                    # Fallback to DELETE if TRUNCATE fails
                    transaction.execute(table.delete())
                    print("Exception cleaning up tables in test %s" % e)
        else:
            # For SQLite, use DELETE
            for table in reversed(SQLModel.metadata.sorted_tables):
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
def user_factory(db_session, is_active=True):
    def _create_user(
        user_id="123", user_email="user@example.com", start_date=datetime(2000, 1, 1), is_active=is_active, role="jobseeker"
    ):
        user = Users(user_id=user_id, user_email=user_email, start_date=start_date, is_active=is_active, role=role)
        db_session.add(user)
        db_session.commit()
        return user

    return _create_user


@pytest.fixture
def logged_in_user(user_factory):
    return user_factory()

@pytest.fixture
def inactive_user(user_factory):
    return user_factory(is_active=False)

@pytest.fixture
def coach_user(user_factory):
    return user_factory(user_id="coach123", user_email="coach@example.com", role="coach")

@pytest.fixture
def client_user(user_factory):
    return user_factory(user_id="client123", user_email="client@example.com", role="jobseeker")

@pytest.fixture
def coach_client_link(coach_user, client_user, db_session):
    link = CoachClientLink(coach_id=coach_user.user_id, client_id=client_user.user_id)
    db_session.add(link)
    db_session.commit()
    return link

@pytest.fixture
def logged_in_coach_client(client_factory, coach_user):
    return client_factory(user=coach_user)


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
        if user and user.is_active:
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
