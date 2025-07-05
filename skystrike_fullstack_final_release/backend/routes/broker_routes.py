# backend/routes/broker_routes.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from ..auth import get_current_user, User
from ..services.tradier_api import (
    get_quote,
    get_balances,
    get_open_pnl as get_positions,
    get_open_orders as get_orders,
)

router = APIRouter(
    prefix="/api/broker",
    tags=["broker"],
)

@router.get("/positions", summary="Get open positions")
async def positions(current_user: User = Depends(get_current_user)):
    try:
        data = get_positions()
        return JSONResponse(content={"positions": data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/balances", summary="Get account balances")
async def balances(current_user: User = Depends(get_current_user)):
    try:
        data = get_balances()
        return JSONResponse(content={"balances": data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/orders", summary="Get open orders")
async def open_orders(current_user: User = Depends(get_current_user)):
    try:
        data = get_orders()
        return JSONResponse(content={"orders": data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/quote/{symbol}", summary="Get quote for a symbol")
async def quote(symbol: str, current_user: User = Depends(get_current_user)):
    try:
        price = get_quote(symbol)
        return JSONResponse(content={"price": price})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
