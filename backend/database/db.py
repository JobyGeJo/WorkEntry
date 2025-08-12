# db.py
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker, declarative_base, DeclarativeMeta, Session
from os import getenv

import logging
from logger import log_db_event
from logger.config import get_rotating_handler

DB_NAME = getenv('POSTGRES_DB')
DB_PASS = getenv('POSTGRES_PASSWORD')
DB_HOST = getenv('HOST')

DATABASE_URL = f"postgresql://{DB_NAME}:{DB_PASS}@{DB_HOST}/postgres"

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
    def __init__(self) -> None:
        self.db: Session = SessionLocal()
        log_db_event("Database initialized")

    def __enter__(self) -> Session:
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.db.close()
        log_db_event("Database closed")

