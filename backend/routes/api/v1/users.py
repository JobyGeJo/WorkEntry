from fastapi import APIRouter
from fastapi.params import Depends
from starlette.responses import JSONResponse

from Enums import Roles
from models.request.params import UserParams
from models.response import Respond
from modules.users import fetch_users
from utils.authorization import required_roles

users = APIRouter(prefix="/users", tags=["users"], dependencies=[Depends(required_roles(Roles.ADMIN, Roles.MANAGER))])

@users.get("")
def get_users(params: UserParams = Depends()) -> JSONResponse:
    return Respond.success("Users fetched successfully", fetch_users(params), pagination=params.pagination)

@users.get("/{user_id}")
def get_user(user_id: int) -> JSONResponse:
    return Respond.success("User data fetched successfully", get_user(user_id))