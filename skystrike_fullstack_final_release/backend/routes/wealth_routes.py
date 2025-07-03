from fastapi import APIRouter, Depends, HTTPException
from backend.auth import get_current_user, User
from backend.utils.cash_balance import get_cash_balance

router = APIRouter(prefix="/wealth", tags=["wealth"])

@router.get("/cash")
async def get_cash(current_user: User = Depends(get_current_user)):
    try:
        return get_cash_balance()
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))
