from fastapi import APIRouter
from pydantic import BaseModel
core.users import update_user

router = APIRouter(prefix="/api")

class ProfileUpdate(BaseModel):
    goal: str = None
    tradier_token: str = None
    tradier_mode: str = None

@router.patch("/profile/{username}")
def patch_profile(username: str, update: ProfileUpdate):
    if update_user(username, update.dict(exclude_none=True)):
        return {"status": "updated"}
    return {"status": "not found"}
