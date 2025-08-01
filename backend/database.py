import os
from typing import Annotated
from sqlmodel import SQLModel, create_engine, Session
from utils.config_utils import get_settings
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import fastapi
import logging

logger = logging.getLogger(__name__)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)


def request_session():
    session = get_session()
    try:
        yield session
    finally:
        session.close()


DBSession = Annotated[Session, fastapi.Depends(request_session)]

settings = get_settings()
IS_DOCKER_CONTAINER = os.environ.get("IS_DOCKER_CONTAINER", 0)
logger.info("IS_DOCKER_CONTAINER: %s", IS_DOCKER_CONTAINER)
if IS_DOCKER_CONTAINER and not settings.is_publicly_deployed:
    logger.info("Using DATABASE_URL_DOCKER for locally deployed environment")
    DATABASE_URL = settings.DATABASE_URL_DOCKER
elif settings.is_publicly_deployed:
    logger.info("Using DATABASE_URL for publicly deployed environment")
    DATABASE_URL = settings.DATABASE_URL
else:
    logger.info("Using DATABASE_URL_LOCAL_VIRTUAL_ENV for locally deployed environment")
    DATABASE_URL = settings.DATABASE_URL_LOCAL_VIRTUAL_ENV

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()