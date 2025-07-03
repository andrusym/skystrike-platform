from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
auth import verify_token
services.tradier_api import get_open_positions
import asyncio

router = APIRouter()

@router.get("/api/broker/positions")
def get_positions(user=Depends(verify_token)):
    try:
        data = asyncio.run(get_open_positions())
        return JSONResponse(content={"positions": data})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
