import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from settings.config import settings


Base = declarative_base()


engine = create_engine(settings.db_url, connect_args={'check_same_thread': False}, echo=True)


def get_db():
    db_session_local = SessionLocal()
    try:
        yield db_session_local
    finally:
        db_session_local.close()


SessionLocal = sessionmaker(expire_on_commit=False, autoflush=False, bind=engine)
