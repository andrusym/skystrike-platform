import os
import jwt
from fastapi import Header, HTTPException, status

# Load JWT secret from environment variable, with a safe fallback
SECRET_KEY = os.getenv("JWT_SECRET", "your-very-secret-key")

def verify_token(auth: str = Header(None)):
    """
    Verify JWT token extracted from Authorization header.
    
    Args:
        auth (str): The value of the Authorization header.

    Returns:
        dict: Decoded JWT payload if token is valid.

    Raises:
        HTTPException: If token is missing, invalid, or expired.
    """
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Missing or invalid token"
        )
    
    token = auth.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token"
        )
