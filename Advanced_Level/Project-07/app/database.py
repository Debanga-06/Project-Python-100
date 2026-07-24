"""
Sets up the SQLAlchemy engine, session, and declarative base.

Using SQLite here so the whole thing runs with zero external setup - just
run the app and library.db gets created automatically. Swapping to
Postgres/MySQL later is just a matter of changing DATABASE_URL, nothing
else in the project needs to change.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./library.db")

# check_same_thread is only needed for SQLite since it's not thread-safe by
# default, and FastAPI can handle a request in a different thread than it
# was created in.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency for routes - opens a session, closes it when the request is done."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
