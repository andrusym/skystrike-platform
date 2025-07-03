from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
core.users import create_user

router = APIRouter()  # ? No prefix here — handled by main.py

class RegisterRequest(BaseModel):
    username: str
    password: str

@router.post("/register")
def register(req: RegisterRequest):
    if not create_user(req.username, req.password):
        raise HTTPException(status_code=400, detail="Username already exists")
    return {"message": "User registered successfully"}
