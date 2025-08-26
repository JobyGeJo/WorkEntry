from starlette.middleware.cors import CORSMiddleware
from routes import app

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://192.168.1.20:5173",  # your real LAN IP here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] for all origins (less secure)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import redis
from database.redis import get_redis_client, host
from logger import log
import logging

try:
    get_redis_client().ping()
    log(f"Redis connection successful!")
except redis.RedisError as e:
    log(f"Failed to connect to the Redis: {e}", logging.ERROR)
    raise ConnectionError(f"Cannot connect to Redis at {host}: {e}")

from database.postgres.connection import engine
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    log("Database connection successful!")
except OperationalError as e:
    log(f"Failed to connect to the database: {e}", logging.ERROR)