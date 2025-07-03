# backend/routes/lifecycle_routes.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import os
import json
import datetime

from backend.auth import get_current_user, User

router = APIRouter(prefix="/api/lifecycle", tags=["lifecycle"])

LIFECYCLE_PATH = os.path.join("config", "bot_lifecycle.json")
DEFAULT_COOLDOWN_MINUTES = 60


@router.get("/status", summary="Fetch bot lifecycle data")
async def get_lifecycle_status(user: User = Depends(get_current_user)):
    """
    Returns raw lifecycle entries, adding calculated cooldown_until if in cooldown.
    """
    try:
        if not os.path.exists(LIFECYCLE_PATH):
            raise FileNotFoundError("bot_lifecycle.json not found")

        with open(LIFECYCLE_PATH, "r") as f:
            data = json.load(f)

        # Compute cooldown_until for entries in cooldown
        for bot_name, entry in data.items():
            if entry.get("status") == "cooldown" and entry.get("last_triggered"):
                ts = entry["last_triggered"]
                dt = datetime.datetime.fromisoformat(ts)
                expiry = dt + datetime.timedelta(minutes=DEFAULT_COOLDOWN_MINUTES)
                entry["cooldown_until"] = expiry.isoformat()

        return JSONResponse(content=data)

    except FileNotFoundError as fnf:
        raise HTTPException(status_code=500, detail=str(fnf))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class LifecycleUpdate(BaseModel):
    status: Optional[str] = None
    last_triggered: Optional[str] = None
    fallback_active: Optional[bool] = None


@router.patch("/status", summary="Update bot lifecycle entries")
async def update_lifecycle(
    updates: dict[str, LifecycleUpdate],
    user: User = Depends(get_current_user)
):
    """
    Applies partial updates to each bot's lifecycle record.
    Expects a mapping like:
    {
      "ironcondor": { "status": "cooldown", "last_triggered": "2025-06-25T20:00:00" },
      "kingcondor": { "fallback_active": true }
    }
    """
    try:
        # Load existing or start fresh
        existing = {}
        if os.path.exists(LIFECYCLE_PATH):
            with open(LIFECYCLE_PATH, "r") as f:
                existing = json.load(f)

        # Apply updates
        for bot_name, upd in updates.items():
            entry = existing.get(bot_name, {})
            if upd.status is not None:
                entry["status"] = upd.status
            if upd.last_triggered is not None:
                entry["last_triggered"] = upd.last_triggered
            if upd.fallback_active is not None:
                entry["fallback_active"] = upd.fallback_active
            existing[bot_name] = entry

        # Persist back to file
        os.makedirs(os.path.dirname(LIFECYCLE_PATH), exist_ok=True)
        with open(LIFECYCLE_PATH, "w") as f:
            json.dump(existing, f, indent=2)

        return JSONResponse(content={"message": "Lifecycle data updated"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
