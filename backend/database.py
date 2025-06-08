import os
from typing import Annotated
from sqlmodel import SQLModel, create_engine, Session
from utils.config_utils import get_settings
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import fastapi


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)


def request_session():
    session = get_session()

    with session.begin():
        yield session


DBSession = Annotated[Session, fastapi.Depends(request_session)]

settings = get_settings()
IS_DOCKER_CONTAINER = os.environ.get("IS_DOCKER_CONTAINER", 0)
if IS_DOCKER_CONTAINER:
    DATABASE_URL = settings.DATABASE_URL_DOCKER
elif settings.is_publicly_deployed:
    DATABASE_URL = settings.DATABASE_URL
else:
    DATABASE_URL = settings.DATABASE_URL_LOCAL_VIRTUAL_ENV

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()