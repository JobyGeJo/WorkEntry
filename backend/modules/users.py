from functools import wraps
from typing import Optional

from sqlalchemy.engine.row import Row
from sqlalchemy.exc import IntegrityError

from Enums import Roles
from Exceptions import NotFound, Unauthorized, Conflict, InternalServerError
from database import with_postgres
from database.postgres import Session, DBSession
from database.postgres.tables import UserTable, RoleTable
from models.models import User
from models.request import RegisterPayload
from models.request.params import UserParams
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



@with_postgres
@model_validate
def get_user(user_id: int, *, db: Session) -> User:
    data = db.query(
        UserTable
    ).filter(
        UserTable.id == user_id
    ).first()

    if data is None:
        raise NotFound("User not found")

    return data

@with_postgres
def login_user(user_id: int, password: str, *, db: Session) -> Optional[User]:
    fetched_password: Row = db.query(UserTable.password).filter(UserTable.id == user_id).first()

    if fetched_password is None:
        raise NotFound("User not found")
    elif verify_password(password, fetched_password.password):
        return get_user(user_id, db=db)
    else:
        raise Unauthorized("Incorrect password")

@with_postgres
@model_validate
def fetch_users(params: UserParams, *, db: Session) -> list[User]:
    return params.build(db.query(UserTable)).all()

@with_postgres
def does_user_exist(user_id: int, *, db: Session) -> bool:
    return bool(db.query(UserTable.id).filter(UserTable.id == user_id).first())

@with_postgres
def create_user(user: RegisterPayload | UserTable, *, db: Session) -> int:
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

@with_postgres
def get_role(user_id: int, *, db: Session) -> Roles:
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