from functools import wraps
from database.db import DBSession

def with_db_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'db' in kwargs:
            return func(*args, **kwargs)

        with DBSession() as session:
            return func(*args, db=session, **kwargs)
    return wrapper
