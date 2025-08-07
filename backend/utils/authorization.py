from typing import List, Callable

from fastapi import Request
from fastapi.params import Depends

from Exceptions import Unauthorized, Forbidden
from logger import log_auth_event
from Enums import AuthEvents, AuthTypes, Roles
from modules.users import get_role
from utils.session import get_session_user_id

def authorize(request: Request, success: str = "Session Authenticated", failed: str = "Session Not Found") -> int:
    current_user: int = get_session_user_id(request)

    if current_user is None:
        log_auth_event(request, AuthTypes.SESSION, AuthEvents.FAILED, None, failed)
        raise Unauthorized(failed)

    log_auth_event(request, AuthTypes.SESSION, AuthEvents.SUCCESS, current_user, success)
    return current_user

def required_roles(*allowed_roles: List[Roles]) -> Callable:

    def check_permission(current_user_id: int = Depends(get_session_user_id)) -> bool:
        role: Roles = get_role(current_user_id)
        if not (role in allowed_roles or role is Roles.ADMIN):
            raise Forbidden("You don't have permission to access this resource")
        return True

    return check_permission