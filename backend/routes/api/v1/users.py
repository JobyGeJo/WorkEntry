from fastapi import APIRouter
from fastapi.params import Depends
from starlette.responses import JSONResponse

from Exceptions import Forbidden
from models.request.params import UserParams
from models.request.payload import UpdateRolesPayload
from models.response import Respond
from modules.users import fetch_users, update_role, fetch_user_details
from utils.authorization import authorize

users = APIRouter(prefix="/users", tags=["users"])

@users.get("")
def get_users(params: UserParams = Depends()) -> JSONResponse:
    return Respond.success("Users fetched successfully", fetch_users(params), pagination=params.pagination)

@users.get("/{user_id}")
def get_user(user_id: int) -> JSONResponse:
    return Respond.success("User data fetched successfully", fetch_user_details(user_id))

# @users.post("", status_code=201)
# def post_user() -> JSONResponse:
#     return Respond.created("User created successfully")

@users.put("/{user_id}/role")
def put_user_role(user_id: int, payload: UpdateRolesPayload, current_user_id: int = Depends(authorize)) -> JSONResponse:
    if user_id == current_user_id:
        raise Forbidden("You cannot update your own role")
    return Respond.success("User role updated successfully", update_role(user_id, payload.role, current_user_id))

# @users.put("/{user_id}")
# def put_user(user_id: int, payload: UserUpdatePayload, current_user: Tuple[Roles, int] = (Depends(get_user_role), Depends(authorize))) -> JSONResponse:
#     if user_id != current_user or current_user[0] < Roles.ADMIN:
#         raise Forbidden("You are not allowed to update this user")
#     return Respond.success("User data updated successfully", update_user_details(user_id, payload))