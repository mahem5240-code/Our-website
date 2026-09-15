"""
Database engine and session configuration.

Works with either SQLite (default, zero-config) or PostgreSQL
(recommended for production) — just change DATABASE_URL in .env.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

# SQLite needs a special connect argument to work with FastAPI's
# multi-threaded request handling. PostgreSQL does not need this.
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    FastAPI dependency that provides a database session per request
    and always closes it afterwards, even if an error occurs.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
