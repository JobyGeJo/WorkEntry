import time
from typing import Optional
from jose import JWTError, jwt

from Exceptions import Unauthorized
from modules.users import fetch_user

# You should store this securely (e.g., in environment variables)
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 60

def create_access_token(data: dict, expires_delta: int = None):
    to_encode = data.copy()
    print(int(time.time()))
    expire = int(time.time()) + (expires_delta or ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    print(to_encode)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id = payload.get("sub")
        print(payload.get("exp") - int(time.time()))
        if not user_id:
            raise JWTError
        return payload
    except JWTError:
        raise Unauthorized("Invalid or expired token")

from fastapi import Header
from fastapi.security import HTTPBearer

security = HTTPBearer()


def get_current_user(Authorization: Optional[str] = Header(None)):
    if not Authorization or not Authorization.startswith("Bearer "):
        raise Unauthorized("Invalid token")

    token = Authorization.split(" ")[1]
    user_id = verify_token(token)["sub"]
    user = fetch_user(user_id)
    if not user:
        raise Unauthorized("User not found")
    return user


if __name__ == "__main__":
    tkn = create_access_token({"sub" : "6", "name" : "Alice"})
    print(tkn)
    print(verify_token(tkn))
    print(int(time.time()))
    print(get_current_user(tkn).username)