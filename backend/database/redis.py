import logging
from logger import log

import redis
import os
from functools import wraps

host = os.getenv('HOST')
if not host:
    raise EnvironmentError("HOST environment variable not set")

_redis_client = redis.Redis(host=os.getenv('HOST'), port=6379, db=0)

try:
    _redis_client.ping()
    log(f"Redis connection successful!")
except redis.RedisError as e:
    log(f"Failed to connect to the Redis: {e}", logging.ERROR)
    raise ConnectionError(f"Cannot connect to Redis at {host}: {e}")

def with_redis(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Allow passing custom client if needed
        if 'r' in kwargs:
            return func(*args, **kwargs)

        return func(*args, r=_redis_client, **kwargs)
    return wrapper

def get_redis_client() -> redis.Redis:
    return _redis_client