import logging
from typing import Any

from fastapi import Request

from Enums import AuthTypes, AuthEvents
from Exceptions import ResponseError, InternalServerError
from .config import get_rotating_handler

app_logger = logging.getLogger("app_logger")
app_logger.setLevel(logging.DEBUG)
app_logger.addHandler(get_rotating_handler("app.log"))

def log_request(request: Request, status_code, duration_ms) -> None:
    msg = f"{request.client.host} - \"{request.method} {request.url.path}?{request.url.query}\" - {duration_ms:.2f}ms - status {status_code}"
    app_logger.info(msg)

def log_auth_event(request: Request, auth_type: AuthTypes, auth_event: AuthEvents, user_id: int | None, reason: str) -> None:
    msg = f"{request.client.host} - {auth_type.value} - status:{auth_event.value} - user:{user_id} - reason:{reason if reason else 'NIL'}"
    level = logging.DEBUG if auth_type is AuthTypes.SESSION else logging.INFO
    level = level if auth_event is AuthEvents.SUCCESS else logging.WARN
    app_logger.log(level, msg)

def log_error(request: Request, error: ResponseError, level: logging = logging.WARN) -> None:
    msg = f"{request.client.host} - \"{request.method} {request.url.path}?{request.url.query}\" - Exception: {type(error).__name__}"
    level = level or logging.ERROR if isinstance(error, InternalServerError) else logging.WARN
    app_logger.log(level, msg)

def log_critical(request: Request, error: Exception) -> None:
    log_error(request, InternalServerError(str(error)), logging.CRITICAL)

def log_debug(text: Any) -> None:
    app_logger.debug(text)

def log(message: str, level=logging.INFO) -> None:
    app_logger.log(level, message)