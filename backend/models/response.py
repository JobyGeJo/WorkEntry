from http import HTTPStatus
from typing import Optional, Dict, Union, Self

from fastapi.responses import JSONResponse
from pydantic import BaseModel, model_validator, computed_field, Field

from Exceptions import ResponseError, UnprocessableContent, NotFound
from utils.session import delete_cookie


class Pagination(BaseModel):
    total_items: int = Field(..., ge=0)
    limit: int = Field(..., gt=0)
    page: int = Field(..., gt=0)

    @computed_field
    def total_pages(self) -> int:
        if self.total_items == 0:
            raise NotFound("No data found")
        pages = (self.total_items + self.limit - 1) // self.limit
        if pages < self.page:
            raise UnprocessableContent(f"Page number {self.page} is out of range. Valid pages are 1 to {pages}.")
        return pages


class ResponseModel[T](BaseModel):
    status: HTTPStatus
    message: str
    data: Optional[T] = None
    pagination: Optional[Pagination] = None

    error: Optional[str] = None
    issues: Optional[Union[str, Dict[str, str]]] = None

    @model_validator(mode='after')
    def validate_based_on_status(self) -> Self:
        if 200 <= self.status < 300:
            # Success response: must have data, no error/issue
            if self.error is not None or self.issues is not None:
                raise ValueError(f"For success status {self.status}, 'error' and 'issues' must be None.")
        else:
            # Error response: must not have data, should have error/issue
            if self.error is None:
                raise ValueError(f"For error status {self.status}, either 'error' or 'issues' must be provided.")
        return self

    # noinspection SpellCheckingInspection
    def jsonresponse(self, **kwargs) -> JSONResponse:
        if 'status_code' not in kwargs:
            kwargs['status_code'] = self.status
        return JSONResponse(self.model_dump(exclude_none=True, mode='json'), **kwargs)


class Respond:

    @staticmethod
    def __send_response[T](
            status: HTTPStatus,
            message: str,
            data: Optional[T] = None,
            pagination: Optional[Pagination] = None,
            **kwargs
    ) -> JSONResponse:
        return ResponseModel(status=status, message=message, data=data, pagination=pagination).jsonresponse(**kwargs)

    @staticmethod
    def __send_error(status: HTTPStatus, message: str,
                     issues: Optional[Union[str, Dict[str, str]]] = None) -> JSONResponse:
        return ResponseModel(status=status, error=status.phrase, message=message, issues=issues).jsonresponse()

    @staticmethod
    def success[T](message: str, data: Optional[T] = None, pagination: Optional[Pagination] = None, **kwargs) -> JSONResponse:
        return Respond.__send_response(HTTPStatus.OK, message, data, pagination, **kwargs)

    @staticmethod
    def created[T](message: str, data: Optional[T] = None, **kwargs) -> JSONResponse:
        return Respond.__send_response(HTTPStatus.CREATED, message, data, **kwargs)

    @staticmethod
    def bad_request(message: str) -> JSONResponse:
        return Respond.__send_error(HTTPStatus.BAD_REQUEST, message)

    @staticmethod
    def unauthorized(message: str, should_delete_cookie: bool = False) -> JSONResponse:
        response = Respond.__send_error(HTTPStatus.UNAUTHORIZED, message)
        if should_delete_cookie:
            delete_cookie(response)
        return response

    @staticmethod
    def forbidden(message: str) -> JSONResponse:
        return Respond.__send_error(HTTPStatus.FORBIDDEN, message)

    @staticmethod
    def not_found(message: str) -> JSONResponse:
        return Respond.__send_error(HTTPStatus.NOT_FOUND, message)

    @staticmethod
    def method_not_allowed(message: str) -> JSONResponse:
        return Respond.__send_error(HTTPStatus.METHOD_NOT_ALLOWED, message)

    @staticmethod
    def unprocessable_content(issues: Dict[str, str]) -> JSONResponse:
        return Respond.__send_error(HTTPStatus.UNPROCESSABLE_CONTENT, "Invalid Parameters", issues)

    @staticmethod
    def internal_server_error(message: str) -> JSONResponse:
        return Respond.__send_error(HTTPStatus.INTERNAL_SERVER_ERROR, message)

    @staticmethod
    def send_error(exc: ResponseError) -> JSONResponse:
        return Respond.__send_error(exc.status, exc.detail)
