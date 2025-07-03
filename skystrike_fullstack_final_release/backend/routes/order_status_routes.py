# backend/routes/order_status_routes.py

from fastapi import APIRouter, Depends, HTTPException, Query
from backend.auth import get_current_user, User
from backend.services.tradier_api import fetch_order_status

router = APIRouter(prefix="/api/orders", tags=["orders"])

@router.get("/status", summary="Get Tradier order status")
async def order_status(
    order_id: str = Query(..., description="The ID of the order to fetch"),
    user: User = Depends(get_current_user)
):
    """
    Returns the status for a given Tradier order_id.
    """
    try:
        return await fetch_order_status(order_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
