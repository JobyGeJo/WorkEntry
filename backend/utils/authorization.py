from typing import List, Callable

from fastapi import Request
from fastapi.params import Depends

from Exceptions import Unauthorized, Forbidden, BadRequest
from logger import log_auth_event
from Enums import AuthEvents, AuthTypes, Roles
from modules.users import get_role, validate_api_key
from utils.session import get_session_user_id, SESSION_COOKIE_NAME


def authorize(request: Request) -> None:
    if "API-Key" in request.headers:
        authorize_by_api_key(request)

    # elif "Authorization" in request.headers:
    #     authorize_by_session(request)

    elif SESSION_COOKIE_NAME in request.cookies:
        authorize_by_session(request)

    else:
        raise Unauthorized("Authentication Required")

def authorize_by_session(request: Request) -> None:
    try:
        current_user: int = get_session_user_id(request)
        log_auth_event(request, AuthTypes.SESSION, AuthEvents.SUCCESS, current_user, "Session Authenticated")

    except (BadRequest, Unauthorized) as e:
        log_auth_event(request, AuthTypes.SESSION, AuthEvents.FAILED, None, e.detail)
        raise e

def authorize_by_api_key(request: Request) -> None:
    api_key: str = request.headers.get("API-Key")
    validate_api_key(api_key)

def required_roles(*allowed_roles: List[Roles]) -> Callable:

    def check_permission(request: Request) -> bool:
        current_user_id: int = get_session_user_id(request)
        role: Roles = get_role(current_user_id)
        if not (role in allowed_roles or role is Roles.ADMIN):
            raise Forbidden("You don't have permission to access this resource")
        return True

    return check_permission