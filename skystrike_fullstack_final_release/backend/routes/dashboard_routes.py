from fastapi import APIRouter, Depends, HTTPException
from backend.dependencies.auth import get_current_user, User
from backend.services.tradier_api import get_open_pnl

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/")
def get_dashboard(current_user: User = Depends(get_current_user)):
    """
    Proxy to Tradier /positions for your paper account.
    """
    try:
        return get_open_pnl()
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))
