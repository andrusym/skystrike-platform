from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
import json, traceback
from backend.dependencies.auth import create_jwt_token, User

class LoginPayload(BaseModel):
    username: str
    password: str

router = APIRouter(tags=["auth"])

@router.post("/login", status_code=status.HTTP_200_OK)
async def login(request: LoginPayload):
    try:
        # load users
        with open("backend/db/users.json", "r") as f:
            users = json.load(f)

        user = users.get(request.username)
        if not user or user["password"] != request.password:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        # assemble user info
        user_info = {
            "username":     request.username,
            "goal":         user.get("goal", "balanced"),
            "account_size": user.get("account_size", 25000),
            "tradier_mode": user.get("tradier_mode", "paper")
        }

        # create JWT with a top-level "user" claim
        token = create_jwt_token({"user": user_info})

        return {
            "access_token": token,
            "token_type":   "bearer",
            "user":         user_info
        }

    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")
