from fastapi import APIRouter, HTTPException
from backend.services.tradier_api import get_quote, get_expirations

router = APIRouter()

@router.get("/quote")
def quote(symbol: str):
    try:
        return get_quote(symbol)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/expirations")
def expirations(symbol: str):
    try:
        return get_expirations(symbol)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
