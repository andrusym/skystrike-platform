# backend/dependencies/auth.py

import os
import jwt
from dotenv import load_dotenv
from datetime import datetime, timedelta
from fastapi import Header, HTTPException, status
from pydantic import BaseModel

# Load environment variables from .env
env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
load_dotenv(dotenv_path=env_path, override=True)

# JWT config
SECRET_KEY = os.getenv("JWT_SECRET", "supersecretkey123")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
EXPIRE_HOURS = int(os.getenv("ACCESS_TOKEN_EXPIRE_HOURS", "12"))


class User(BaseModel):
    """
    Represents an authenticated user (the "user" claim in the JWT).
    """
    username: str
    goal: str
    account_size: float
    tradier_mode: str


def create_jwt_token(
    data: dict,
    expires_delta: timedelta = timedelta(hours=EXPIRE_HOURS)
) -> str:
    """
    Create a JWT encoding the provided `data` payload (must include a top-level "user" key)
    and set to expire after `expires_delta`.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_jwt_token(token: str) -> dict:
    """
    Decode and verify a JWT, returning its payload dict.
    """
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


async def get_current_user(
    authorization: str = Header(...)
) -> User:
    """
    FastAPI dependency. Extracts the Bearer token, decodes it, and returns a User model.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization header")

    token = authorization.split(" ", 1)[1]

    try:
        payload = decode_jwt_token(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user_data = payload.get("user")
    if not user_data or not isinstance(user_data, dict):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Malformed token payload")

    return User(**user_data)
