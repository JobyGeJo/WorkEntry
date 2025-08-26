import redis
import os
from functools import wraps

host = os.getenv('REDIS_HOST')
if not host:
    raise EnvironmentError("HOST environment variable not set")

_redis_client = redis.Redis(host=host, port=6379, db=0)

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