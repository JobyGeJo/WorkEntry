
from fastapi import APIRouter, Request, Response, Depends

from Enums import Roles
from Exceptions import BadRequest
from models.models import User
from models.request import LoginPayload, RegisterPayload
from models.response import Respond

from modules.users import get_user, login_user, create_user
from utils.authorization import authorize, required_roles
from utils.session import create_session, get_session_user_id, delete_session, SESSION_COOKIE_NAME, is_session_valid

router = APIRouter(prefix="/v1")


@router.post("/login")
def login(request: Request, response: Response, payload: LoginPayload):
    session_id = request.cookies.get(SESSION_COOKIE_NAME)
    if session_id is not None and is_session_valid(session_id):
        raise BadRequest("Existing Session Found")

    user = login_user(payload.id, payload.password)
    create_session(payload.id, response)
    return Respond.success("Logged in successfully", user, headers=response.headers)


@router.post("/register", status_code=201)
def register(response: Response, payload: RegisterPayload):
    user_id = create_user(payload)
    # create_session(user_id, response)
    return Respond.created("Registered successfully", {"user_id": user_id}, headers=response.headers)


@router.get("/session")
def session(request: Request):
    user_id = get_session_user_id(request)
    return Respond.success("Session Found Successfully", get_user(user_id))


@router.post("/logout", dependencies=[Depends(authorize)])
def logout(request: Request, response: Response):
    delete_session(request, response)
    return Respond.success("Logged out successfully", headers=response.headers)

