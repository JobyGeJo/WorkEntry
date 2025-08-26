from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker, declarative_base, DeclarativeMeta, Session
from os import getenv

import logging
from logger import log_db_event, log
from logger.config import get_rotating_handler

DB_NAME = getenv('POSTGRES_DB')
DB_USER = getenv('POSTGRES_USER')
DB_PASS = getenv('POSTGRES_PASSWORD')
DB_HOST = getenv('POSTGRES_HOST')

missing_vars = [var_name for var_name, var_value in {
    'POSTGRES_DB': DB_NAME,
    'POSTGRES_USER': DB_USER,
    'POSTGRES_PASSWORD': DB_PASS,
    'POSTGRES_HOST': DB_HOST
}.items() if not var_value]

if missing_vars:
    raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

engine: Engine = create_engine(DATABASE_URL)
SessionLocal: sessionmaker = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base: DeclarativeMeta = declarative_base()

# Suppress noisy sub-loggers
logging.getLogger('sqlalchemy.pool').setLevel(logging.WARNING)
logging.getLogger('sqlalchemy.dialects').setLevel(logging.WARNING)
logging.getLogger('sqlalchemy.engine.Engine').setLevel(logging.INFO)
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Add rotating file handler only to core engine
sqlalchemy_logger = logging.getLogger('sqlalchemy.engine')
sqlalchemy_logger.addHandler(get_rotating_handler("db.log", logging.INFO))

class DBSession:
    """
    Manages a database session lifecycle.

    This class provides context management support for handling database
    sessions. It initializes a database session upon entry, logs the
    initialization event, and ensures the session is properly closed and
    logged after use.

    Attributes:
        db: A Session instance representing the current database session.

    Methods:
        __init__: Initializes the DBSession instance and creates a
            Session object.
        __enter__: Opens and returns the database session.
        __exit__: Closes the database session and logs its closure.
    """
    def __init__(self) -> None:
        self.db: Session = SessionLocal()
        log_db_event("Database initialized")

    def __enter__(self) -> Session:
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.db.close()
        log_db_event("Database closed")
