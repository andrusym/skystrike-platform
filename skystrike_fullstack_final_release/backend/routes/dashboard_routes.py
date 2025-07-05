# backend/routes/dashboard_routes.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

# Correct import paths
from ..auth import get_current_user, User
from ..services.dashboard import (
    get_dashboard_metrics,
    get_strategy_status,
)

router = APIRouter(
    prefix="/api/dashboard",
    tags=["dashboard"],
)

@router.get("/", summary="Fetch overall dashboard metrics")
async def dashboard(current_user: User = Depends(get_current_user)):
    """
    Retrieve system health, P&L, and performance summary for display.
    """
    try:
        metrics = get_dashboard_metrics()
        return JSONResponse(content={"metrics": metrics})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/strategies", summary="Fetch strategy status details")
async def strategies_status(current_user: User = Depends(get_current_user)):
    """
    Retrieve individual bot status (active, cooldown, P&L, win rate, etc.).
    """
    try:
        status = get_strategy_status()
        return JSONResponse(content={"strategies": status})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
