import bcrypt

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


if __name__ == "__main__":
    Password = "12345678"

    hashed = hash_password(Password)
    print(hashed)
    print(verify_password(Password, hashed))