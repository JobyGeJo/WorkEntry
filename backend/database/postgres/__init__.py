from functools import wraps
from .connection import DBSession, Session

def with_postgres(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'db' in kwargs:
            return func(*args, **kwargs)

        with DBSession() as session:
            return func(*args, db=session, **kwargs)
    return wrapper