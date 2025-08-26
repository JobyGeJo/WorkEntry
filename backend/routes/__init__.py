# main.py
import time

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse

from Exceptions import ResponseError, UnprocessableContent, Unauthorized
from logger import log_request, log_error
from logger.app import log_critical
from models.response import Respond
from routes.api import api_router
# from routes.utils import router as utils_router
from routes.auth import router as auth_router

app = FastAPI()

# Include auth routes with optional prefix
app.include_router(auth_router)
app.include_router(api_router)
# app.include_router(utils_router)

@app.exception_handler(ResponseError)
def response_exception_handler(request: Request, exc: ResponseError) -> JSONResponse:
    log_error(request, exc)
    if isinstance(exc, Unauthorized):
        return Respond.unauthorized(exc.detail, exc.delete_cookie)
    return Respond.send_error(exc)

@app.exception_handler(RequestValidationError)
def request_validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    issues = {
        err["loc"][-1]: err["msg"] for err in exc.errors()
    }
    error = UnprocessableContent("Invalid Parameters")
    log_error(request, error)
    return Respond.unprocessable_content(issues)

@app.exception_handler(Exception)
def exception_handler(request: Request, exc: Exception) -> JSONResponse:
    log_critical(request, exc)
    return Respond.internal_server_error(type(exc).__name__)

@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = (time.time() - start_time) * 1000
    log_request(request, response.status_code, duration)
    return response