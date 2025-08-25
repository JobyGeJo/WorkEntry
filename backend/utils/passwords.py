import bcrypt
import secrets

def generate_hash(plaintext_secret: str) -> str:
    """Hashes a plaintext string (password, API key, etc.) using bcrypt."""
    return bcrypt.hashpw(plaintext_secret.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_hash(plaintext_secret: str, hashed_value: str) -> bool:
    """Verifies a plaintext string against a stored bcrypt hash."""
    return bcrypt.checkpw(plaintext_secret.encode("utf-8"), hashed_value.encode("utf-8"))

def generate_random_password() -> str:
    """Generates a random password."""
    return bcrypt.gensalt().decode("utf-8")[-12:]

def generate_api_key() -> str:
    """Generates a random API key."""
    return secrets.token_urlsafe(32)


if __name__ == "__main__":
    print(generate_hash("hashedpassword123"))