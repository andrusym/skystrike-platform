from fastapi import APIRouter
utils.trade_logger import get_trade_log

router = APIRouter()

@router.get("/enhanced")
def get_enhanced_journal():
    trades = get_trade_log()
    return {"trades": trades[-10:]}  # last 10 trades