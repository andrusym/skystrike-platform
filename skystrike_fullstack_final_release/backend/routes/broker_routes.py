from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
auth import verify_token  # ? Fixed import path
services.tradier_api import get_quote, get_account_balances, get_open_positions, get_open_orders
utils.trade_logger import get_trade_log
import asyncio

router = APIRouter()

@router.get("/api/broker/positions")
def positions(user=Depends(verify_token)):
    try:
        data = asyncio.run(get_open_positions())
        return JSONResponse(content={"positions": data})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.get("/api/broker/balances")
def balances(user=Depends(verify_token)):
    try:
        data = asyncio.run(get_account_balances())
        return JSONResponse(content={"balances": data})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.get("/api/broker/orders")
def open_orders(user=Depends(verify_token)):
    try:
        data = asyncio.run(get_open_orders())
        return JSONResponse(content={"orders": data})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.get("/api/broker/quote/{symbol}")
def quote(symbol: str, user=Depends(verify_token)):
    try:
        price = asyncio.run(get_quote(symbol))
        return JSONResponse(content={"price": price})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
