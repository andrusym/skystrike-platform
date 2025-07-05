# backend/routes/bot_metrics_route.py

from fastapi import APIRouter
from backend.utils.trade_logger import get_trade_log

router = APIRouter()

@router.get("/bot_metrics/{bot_name}")
async def bot_metrics(bot_name: str):
    """
    Return the trade log for a given bot.
    """
    log = get_trade_log(bot_name)
    return {"bot": bot_name, "log": log}
