import os
from datetime import datetime, timedelta
from typing import Optional

from dotenv import load_dotenv
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

# Load environment variables from .env
load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET", "supersecretkey123")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_HOURS = int(os.getenv("ACCESS_TOKEN_EXPIRE_HOURS", "12"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")


class User(BaseModel):
    username: str
    goal: str
    account_size: float
    tradier_mode: str


def create_jwt_token(
    *, 
    data: dict, 
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT token that includes a `user` claim and an expiration.
    """
    to_encode = {"user": data.copy()}
    expire = datetime.utcnow() + (
        expires_delta if expires_delta else timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Dependency for FastAPI routes: extracts the current user from the JWT.
    """
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_data = payload.get("user")
        if user_data is None:
            raise credentials_exc
        return User(**user_data)
    except jwt.PyJWTError:
        raise credentials_exc


__all__ = ["create_jwt_token", "get_current_user", "User"]
