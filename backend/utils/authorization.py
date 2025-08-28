from typing import List, Callable, Annotated

from fastapi import Request
from fastapi.params import Depends
from sqlalchemy.sql.functions import current_user

from Exceptions import Unauthorized, Forbidden, BadRequest
from logger import log_auth_event
from Enums import AuthEvents, AuthTypes, Roles
from modules.users import get_role, validate_api_key
from utils.session import get_session_user_id, SESSION_COOKIE_NAME


def authorize(request: Request) -> int:
    if hasattr(request.state, "current_user_id"):
        return request.state.current_user_id

    if "API-Key" in request.headers:
        user_id = authorize_by_api_key(request)

    elif SESSION_COOKIE_NAME in request.cookies:
        user_id = authorize_by_session(request)

    else:
        raise Unauthorized("Authentication Required")

    request.state.current_user_id = user_id
    return user_id

def authorize_by_session(request: Request) -> int:
    try:
        current_user: int = get_session_user_id(request)
        log_auth_event(request, AuthTypes.SESSION, AuthEvents.SUCCESS, current_user, "Session Authenticated")
        return current_user

    except (BadRequest, Unauthorized) as e:
        log_auth_event(request, AuthTypes.SESSION, AuthEvents.FAILED, None, e.detail)
        raise e

def authorize_by_api_key(request: Request) -> int:
    try:
        api_key: str = request.headers.get("API-Key")
        current_user = validate_api_key(api_key)
        log_auth_event(request, AuthTypes.API_KEY, AuthEvents.SUCCESS, current_user, "API Key Authenticated")
        return current_user
    except Unauthorized as e:
        log_auth_event(request, AuthTypes.API_KEY, AuthEvents.FAILED, None, e.detail)
        raise e

def get_user_role(request: Request) -> Roles:
    if hasattr(request.state, "role"):
        role: Roles = request.state.role
    else:
        current_user_id: int = authorize(request)
        role: Roles = get_role(current_user_id)
        request.state.role = role

    return role


def required_roles(*allowed_roles: List[Roles]) -> Callable:

    def check_permission(request: Request) -> bool:
        role: Roles = get_user_role(request)
        if not (role in allowed_roles or role is Roles.ADMIN or role is Roles.OWNER):
            raise Forbidden("You don't have permission to access this resource")
        return True

    return check_permission

Authorize = Annotated[int, Depends(authorize)]
GetUserRole = Annotated[Roles, Depends(get_user_role)]