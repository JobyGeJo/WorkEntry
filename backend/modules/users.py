from functools import wraps

from sqlalchemy.engine.row import Row
from sqlalchemy.exc import IntegrityError

from Enums import Roles
from Exceptions import NotFound, Unauthorized, Conflict, InternalServerError
from database import with_postgres
from database.postgres import Session
from database.postgres.tables import UserTable, RoleTable
from logger import log_db_error
from models.models import User
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
def login_user(user_id: int, password: str, *, db: Session) -> User:
    fetched_password: Row = db.query(UserTable.password).filter(UserTable.id == user_id).first()

    if fetched_password is None:
        raise NotFound("User not found")
    elif verify_hash(password, fetched_password.password):
        return get_user(user_id, db=db)
    else:
        raise Unauthorized("Incorrect password")

@with_postgres
def validate_api_key(api_key: str, *, db: Session) -> int:
    data = db.query(UserTable.id).filter(UserTable.api_key == api_key).one_or_none()
    if data.id is None:
        raise Unauthorized("Invalid API key")
    return data.id

@with_postgres
def get_api_key(user_id: int, *, db: Session) -> str:
    data = db.query(UserTable.api_key).filter(UserTable.id == user_id).one_or_none()
    if data.api_key is None:
        return update_api_key(user_id, db=db)
    return data.api_key

@with_postgres
def update_api_key(user_id: int, *, db: Session) -> str:
    key = generate_api_key()

    try:
        db.query(UserTable).filter(UserTable.id == user_id).update({"api_key": key})
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
    return bool(db.query(UserTable.id).filter(UserTable.id == user_id).one_or_none())

@with_postgres
def create_user(user: RegisterPayload | UserTable, *, db: Session) -> int:
    if isinstance(user, RegisterPayload):
        user = UserTable(
            username=user.username,
            password=generate_hash(user.password),
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