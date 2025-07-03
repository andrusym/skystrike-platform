# backend/routes/config_log_route.py

import os
import json
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from backend.auth import get_current_user, User

router = APIRouter(prefix="/api/config", tags=["config"])

LOG_PATH = os.path.join("logs", "config_change_log.json")


@router.get("/log", summary="Get configuration change log")
async def get_config_log(user: User = Depends(get_current_user)):
    """
    Returns the full configuration change log.
    """
    if not os.path.exists(LOG_PATH):
        raise HTTPException(status_code=404, detail="Configuration change log not found")

    try:
        with open(LOG_PATH, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Invalid JSON in log file: {e}")

    return JSONResponse(content=data)
