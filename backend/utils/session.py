from typing import Optional, List
from redis import Redis
import uuid
from Exceptions import Unauthorized, BadRequest
from fastapi import Response, Request
from Exceptions.ResponseErrors import TooManyRequests
from database import with_redis, get_redis_client

SESSION_COOKIE_NAME = "session_id"
SESSION_EXPIRY_SECONDS = 60 * 5
MAX_SESSIONS = 3

def create_session(user_id: int, response: Response):
    if get_session_count(user_id) >= MAX_SESSIONS:
        raise TooManyRequests(f"The user already has {MAX_SESSIONS} sessions")

    session_id = str(uuid.uuid4())
    _store_session(session_id, user_id)
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=session_id,
        httponly=True,
        samesite="lax",
        secure=False,
    )
    return session_id

@with_redis
def _store_session(session_id: str, user_id: int, *, r: Redis):
    r.setex(f"session:{session_id}", SESSION_EXPIRY_SECONDS, user_id)
    r.sadd(f"user_sessions:{user_id}", session_id)
    r.expire(f"user_sessions:{user_id}", SESSION_EXPIRY_SECONDS)

def get_session_user_id(request: Request) -> int:
    session_id = request.cookies.get(SESSION_COOKIE_NAME)
    if not session_id:
        raise BadRequest("Session Not Found")
    r = get_redis_client()
    user_id: Optional[bytes] = r.get(f"session:{session_id}")
    if not user_id:
        raise Unauthorized("Session Expired or Invalid", True)
    user_id: int = int(user_id)

    r.expire(f"session:{session_id}", SESSION_EXPIRY_SECONDS)
    r.expire(f"user_sessions:{user_id}", SESSION_EXPIRY_SECONDS)

    return user_id

@with_redis
def get_session_count(user_id: int, *, r: Redis) -> int:
    return r.scard(f"user_sessions:{user_id}")

@with_redis
def delete_session(request: Request, response: Response, *, r: Redis) -> None:
    session_id = request.cookies.get(SESSION_COOKIE_NAME)
    if session_id:
        user_id: bytes = r.get(f"session:{session_id}")
        if user_id:
            r.srem(f"user_sessions:{int(user_id)}", session_id)
        r.delete(f"session:{session_id}")
    delete_cookie(response)

def delete_cookie(response: Response) -> None:
    response.delete_cookie(SESSION_COOKIE_NAME)

@with_redis
def is_session_valid(session_id: str, *, r: Redis) -> bool:
    """Check if a session ID is valid (exists and not expired)."""
    return r.exists(f"session:{session_id}") == 1

@with_redis
def get_user_sessions(user_id: int, *, r: Redis) -> List[str]:
    key = f"user_sessions:{user_id}"
    session_ids = r.smembers(key)  # returns set of bytes
    sessions = []

    for session_id in session_ids:
        session_id_str = session_id.decode()
        # Check if session still exists (not expired)
        if r.exists(f"session:{session_id_str}"):
            sessions.append(session_id_str)
        else:
            # Clean up stale session ID reference
            r.srem(key, session_id_str)

    return sessions


if __name__ == "__main__":
    print(get_user_sessions(13))



