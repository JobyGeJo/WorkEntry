from http import HTTPStatus
from typing import Sequence

from fastapi import HTTPException

class ResponseError(HTTPException):
    def __init__(self, status: HTTPStatus, *args, **kwargs):
        self.status = status
        super().__init__(status_code=status.value, *args, **kwargs)

class BadRequest(ResponseError):
    def __init__(self, detail: str) -> None:
        super().__init__(HTTPStatus.BAD_REQUEST, detail=detail)

class Unauthorized(ResponseError):
    def __init__(self, detail: str, delete_cookie: bool = False) -> None:
        self.delete_cookie = delete_cookie
        super().__init__(HTTPStatus.UNAUTHORIZED, detail=detail)

class Forbidden(ResponseError):
    def __init__(self, detail: str) -> None:
        super().__init__(HTTPStatus.FORBIDDEN, detail=detail)

class NotFound(ResponseError):
    def __init__(self, detail: str) -> None:
        super().__init__(HTTPStatus.NOT_FOUND, detail=detail)

class MethodNotAllowed(ResponseError):
    def __init__(self, detail: str) -> None:
        super().__init__(HTTPStatus.METHOD_NOT_ALLOWED, detail=detail)

class Conflict(ResponseError):
    def __init__(self, detail: str) -> None:
        super().__init__(HTTPStatus.CONFLICT, detail=detail)

class UnprocessableContent(ResponseError):
    def __init__(self, detail: str | Sequence) -> None:
        super().__init__(HTTPStatus.UNPROCESSABLE_CONTENT, detail=detail)

class TooManyRequests(ResponseError):
    def __init__(self, detail: str) -> None:
        super().__init__(HTTPStatus.TOO_MANY_REQUESTS, detail=detail)

class InternalServerError(ResponseError):
    def __init__(self, detail: str) -> None:
        super().__init__(HTTPStatus.INTERNAL_SERVER_ERROR, detail=detail)