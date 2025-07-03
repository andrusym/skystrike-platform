# backend/routes/fallback_routes.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import json

from backend.auth import get_current_user, User

router = APIRouter(prefix="/api/fallbacks", tags=["fallbacks"])

LIFECYCLE_PATH = os.path.join("config", "bot_lifecycle.json")


class FallbackUpdate(BaseModel):
    fallback_active: bool


@router.get("/", summary="Get fallback status for all bots")
async def get_fallbacks(user: User = Depends(get_current_user)):
    """
    Returns the `fallback_active` flag for each bot.
    """
    data = {}
    if os.path.exists(LIFECYCLE_PATH):
        with open(LIFECYCLE_PATH, "r") as f:
            lifecycle = json.load(f)
        for bot_name, entry in lifecycle.items():
            data[bot_name] = entry.get("fallback_active", False)
    return JSONResponse(content=data)


@router.patch("/", summary="Update fallback status for multiple bots")
async def patch_fallbacks(
    updates: dict[str, FallbackUpdate],
    user: User = Depends(get_current_user)
):
    """
    Updates `fallback_active` flags. Expects a body like:
    {
      "ironcondor": { "fallback_active": true },
      "gridbot":   { "fallback_active": false }
    }
    """
    lifecycle = {}
    if os.path.exists(LIFECYCLE_PATH):
        with open(LIFECYCLE_PATH, "r") as f:
            lifecycle = json.load(f)

    for bot_name, upd in updates.items():
        entry = lifecycle.get(bot_name, {})
        entry["fallback_active"] = upd.fallback_active
        lifecycle[bot_name] = entry

    os.makedirs(os.path.dirname(LIFECYCLE_PATH), exist_ok=True)
    with open(LIFECYCLE_PATH, "w") as f:
        json.dump(lifecycle, f, indent=2)

    return JSONResponse(content={"message": "Fallback statuses updated", "updates": updates})
