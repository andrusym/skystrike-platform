from fastapi import APIRouter
from backend.utils.trade_logger import get_trade_log

router = APIRouter()


@router.get("/enhanced")
def get_enhanced_journal():
    """
    Returns the last 10 trades from the trade log.
    """
    trades = get_trade_log()
    return {"trades": trades[-10:]}
