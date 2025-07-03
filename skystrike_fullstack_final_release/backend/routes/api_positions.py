from fastapi import APIRouter
from backend.services.tradier_api import get_open_pnl

router = APIRouter()

@router.get("/api/positions")
def get_positions(mode: str = "paper"):
    return get_open_pnl(mode)