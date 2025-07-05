# backend/routes/broker_health_routes.py

from fastapi import APIRouter, Depends, HTTPException
from ..auth import get_current_user, User
from ..services.tradier_client import ping_tradier

router = APIRouter(
    prefix="/api/health",
    tags=["health"],
)

@router.get(
    "/broker",
    summary="Check Tradier broker connectivity"
)
async def broker_health(current_user: User = Depends(get_current_user)):
    """
    Pings the Tradier API to verify broker connectivity.
    Returns 'online' if the ping succeeds, otherwise raises a 503.
    """
    try:
        healthy = ping_tradier()
        return {"tradier": "online" if healthy else "offline"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Tradier ping failed: {e}")
