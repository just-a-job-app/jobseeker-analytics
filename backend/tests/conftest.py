import sys
import os

import pytest
from testcontainers.postgres import PostgresContainer
import sqlalchemy as sa
from sqlalchemy.orm import Session
from sqlmodel import SQLModel

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.chdir("./backend")

import database  # noqa: E402


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:13") as postgres:
        yield postgres


@pytest.fixture
def engine(postgres_container: PostgresContainer, monkeypatch):
    test_engine = sa.create_engine(
        sa.URL.create(
            "postgresql",
            username=postgres_container.username,
            password=postgres_container.password,
            host=postgres_container.get_container_host_ip(),
            port=postgres_container.get_exposed_port(postgres_container.port),
            database=postgres_container.dbname,
        )
    )

    monkeypatch.setattr(database, "engine", test_engine)

    database.create_db_and_tables()

    yield test_engine

    with test_engine.begin() as transaction:
        transaction.execute(
            sa.text("SET session_replication_role = :role"), {"role": "replica"}
        )
        for table in SQLModel.metadata.tables.values():
            transaction.execute(table.delete())


@pytest.fixture
def db_session(engine, monkeypatch):
    with Session(database.engine) as session:
        yield session
