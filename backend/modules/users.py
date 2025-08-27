from functools import wraps
from typing import Optional

from psycopg2.errors import NotNullViolation
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from Enums import Roles
from Exceptions import NotFound, Unauthorized, Conflict, InternalServerError, Forbidden, BadRequest
from database import with_postgres
from database.postgres import Session
from database.postgres.tables import UserTable, UserAccount
from logger import log_db_error
from models.models import User, UserDetail
from models.request import RegisterPayload
from models.request.params import UserParams
from utils.passwords import generate_hash, verify_hash, generate_api_key


def model_validate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        val = func(*args, **kwargs)

        if val is None:
            return None

        elif isinstance(val, UserTable):
            return UserDetail.model_validate(val)

        elif isinstance(val, list) and all(isinstance(i, UserTable) for i in val):
            return [User.model_validate(i) for i in val]

        else:
            raise InternalServerError("Isn't Supposed to happen")

    return wrapper



@with_postgres
@model_validate
def fetch_user(user_id: int, *, db: Session) -> User:
    data = db.query(UserTable).options(joinedload(UserTable.account)).filter(UserTable.user_id == user_id).first()

    if data is None:
        raise NotFound("User not found")

    return data

@with_postgres
def login_user(username: str, password: str, *, db: Session) -> User:
    data: UserAccount = db.query(UserAccount).filter(UserAccount.username == username).one_or_none()

    if data is None:
        raise NotFound("User not found")
    elif verify_hash(password, data.password_hash):
        return fetch_user(data.user_id, db=db)
    else:
        raise Unauthorized("Incorrect password")

@with_postgres
def validate_api_key(api_key: str, *, db: Session) -> int:
    data = db.query(UserAccount.user_id).filter(UserAccount.api_key == api_key).one_or_none()
    if data is None:
        raise Unauthorized("Invalid API key")
    return data.user_id

@with_postgres
def get_api_key(user_id: int, *, db: Session) -> str:
    data = db.query(UserAccount.api_key).filter(UserAccount.user_id == user_id).one_or_none()
    if data.api_key is None:
        return update_api_key(user_id, db=db)
    return data.api_key

@with_postgres
def update_api_key(user_id: int, *, delete: bool = False, db: Session) -> str:
    key = generate_api_key() if not delete else None

    try:
        db.query(UserAccount).filter(UserAccount.user_id == user_id).update({"api_key": key})
    except IntegrityError as e:
        db.rollback()
        log_db_error(e.detail)
        raise InternalServerError("Database error while updating api key")

    db.commit()
    return key

@with_postgres
@model_validate
def fetch_users(params: UserParams, *, db: Session) -> list[User]:
    return params.build(db.query(UserTable)).all()

@with_postgres
def does_user_exist(user_id: int, *, db: Session) -> bool:
    return bool(db.query(UserTable.user_id).filter(UserTable.user_id == user_id).one_or_none())

@with_postgres
def create_user(payload: RegisterPayload, *, db: Session) -> int:
    user: UserTable = UserTable(full_name=payload.full_name)
    user.account = UserAccount(username=payload.username, password_hash=generate_hash(payload.password), role=Roles.USER.value)
    # user.phone_numbers = UserPhoneNumber(phone_number=payload.phone_number)

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user.user_id

    except NotNullViolation as e:
        db.rollback()
        log_db_error(e)
        raise InternalServerError("Database error while creating user")

    except IntegrityError as e:
        db.rollback()

        # noinspection SpellCheckingInspection
        if getattr(e.orig, 'pgcode', None) == "23505":
            raise Conflict("Username already exists")

        raise InternalServerError("Database error while creating user")


@with_postgres
def get_role(user_id: int, *, db: Session) -> Roles:
    data = db.query(UserAccount.role).filter(UserAccount.user_id == user_id).one_or_none()
    if data is None:
        raise NotFound("User not found")
    return Roles(data.role)


@with_postgres
def _update_role(user_id: int, role: Roles, *, db: Session) -> None:
    try:
        db.query(UserAccount).filter(UserAccount.user_id == user_id).update({"role": role})
        db.commit()
    except IntegrityError as e:
        db.rollback()
        log_db_error(e.detail)
        raise InternalServerError("Database error while updating role")


@with_postgres
def set_owner_role(user_id: int, current_user_id: int, *, db: Session) -> None:
    current_user_role = get_role(current_user_id, db=db)

    if current_user_role != Roles.OWNER:
        raise Forbidden("You are not allowed to do this")

    _update_role(user_id=current_user_id, role=Roles.ADMIN, db=db)
    _update_role(user_id=user_id, role=Roles.OWNER, db=db)


@with_postgres
def set_admin_role(user_id: int, current_user_id: int, *, db: Session) -> None:
    current_user_role = get_role(current_user_id, db=db)
    target_user_role = get_role(user_id, db=db)

    if current_user_role < Roles.ADMIN:
        raise Forbidden("You are not allowed to do this")
    elif target_user_role == Roles.OWNER:
        raise Forbidden("You are not allowed to update role of this person")
    elif target_user_role == Roles.ADMIN:
        raise BadRequest("The person already has admin role")

    _update_role(user_id=user_id, role=Roles.ADMIN, db=db)


@with_postgres
def set_manager_role(user_id: int, current_user_id: int, *, db: Session) -> None:
    current_user_role = get_role(current_user_id, db=db)
    target_user_role = get_role(user_id, db=db)

    if current_user_role < Roles.MANAGER:
        raise Forbidden("You are not allowed to do this")
    elif current_user_role == Roles.MANAGER and target_user_role > Roles.MANAGER:
        raise Forbidden("You are not allowed to update role of this person")
    elif current_user_role == Roles.ADMIN and target_user_role == Roles.OWNER:
        raise Forbidden("You are not allowed to update role of this person")
    elif target_user_role == Roles.MANAGER:
        raise BadRequest("The person already has manager role")

    _update_role(user_id=user_id, role=Roles.MANAGER, db=db)


def set_user_role(user_id: int, current_user_id: int, *, db: Session) -> None:
    current_user_role = get_role(current_user_id, db=db)
    target_user_role = get_role(user_id, db=db)

    if target_user_role > current_user_role:
        raise Forbidden("You are not allowed to update role of this person")
    elif target_user_role == Roles.USER:
        raise BadRequest("The person already has user role")

    _update_role(user_id=user_id, role=Roles.USER, db=db)


@with_postgres
def update_role(user_id: int, role: Roles, current_user_id: Optional[int] = None, *, db: Session) -> None:
    match role:
        case Roles.OWNER:
            return set_owner_role(user_id, current_user_id, db=db)
        case Roles.ADMIN:
            return set_admin_role(user_id, current_user_id, db=db)
        case Roles.MANAGER:
            return set_manager_role(user_id, current_user_id, db=db)
        case Roles.USER:
            return set_user_role(user_id, current_user_id, db=db)
        case _:
            raise InternalServerError("Unknown role")

if __name__ == "__main__":
    print(fetch_user(1).json(), sep="\n")