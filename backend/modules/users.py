from functools import wraps
from typing import Optional

from sqlalchemy.engine.row import Row
from sqlalchemy.exc import IntegrityError

from Enums import Roles
from Exceptions import NotFound, Unauthorized, Conflict, InternalServerError
from database import with_db_session
from database.db import SessionLocal
from database.tables import UserTable, RoleTable
from models.models import User
from models.request import RegisterPayload
from utils.passwords import hash_password, verify_password


def model_validate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        val = func(*args, **kwargs)

        if val is None:
            return None

        elif isinstance(val, UserTable):
            return User.model_validate(val)

        elif isinstance(val, list) and all(isinstance(i, UserTable) for i in val):
            return [User.model_validate(i) for i in val]

        else:
            raise InternalServerError("Isn't Supposed to happen")

    return wrapper



@with_db_session
def get_user(user_id: int, *, db: SessionLocal) -> User:
    data = db.query(
        UserTable.id,
        UserTable.username,
        UserTable.phone_number
    ).filter(
        UserTable.id == user_id
    ).first()

    if data is None:
        raise NotFound("User not found")
    else:
        return User(id=data.id, username=data.username, phone_number=data.phone_number)

@with_db_session
def login_user(user_id: int, password: str, *, db: SessionLocal) -> Optional[User]:
    fetched_password: Row = db.query(UserTable.password).filter(UserTable.id == user_id).first()

    if fetched_password is None:
        raise NotFound("User not found")
    elif verify_password(password, fetched_password.password):
        return get_user(user_id, db=db)
    else:
        raise Unauthorized("Incorrect password")

@with_db_session
@model_validate
def find_users(username: str, *, db: SessionLocal) -> list[User]:
    return db.query(UserTable.password, UserTable.username).filter(UserTable.username.contains(username)).all()

@with_db_session
def does_user_exist(user_id: int, *, db: SessionLocal) -> bool:
    return bool(db.query(UserTable.id).filter(UserTable.id == user_id).first())

@with_db_session
def create_user(user: RegisterPayload | UserTable, *, db: SessionLocal) -> int:
    if isinstance(user, RegisterPayload):
        user = UserTable(
            username=user.username,
            password=hash_password(user.password),
            phone_number=user.phone_number,
        )
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user.id

    except IntegrityError as e:
        db.rollback()

        # noinspection SpellCheckingInspection
        if getattr(e.orig, 'pgcode', None) == "23505":
            raise Conflict("Username already exists")

        raise InternalServerError("Database error while creating user")

@with_db_session
def get_role(user_id: int, *, db: SessionLocal) -> Roles:
    role = (
        db.query(RoleTable.label)
        .join(UserTable, UserTable.role_id == RoleTable.id)
        .filter(UserTable.id == user_id)
        .one_or_none()
    )
    if role is None:
        raise NotFound("User not found")
    return Roles(role.label)

if __name__ == "__main__":
    print(get_role(5))