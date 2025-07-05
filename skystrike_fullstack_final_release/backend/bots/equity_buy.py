
import logging
from typing import Dict, Any
from datetime import date, timedelta
from backend.services.tradier_client import TradierClient
from backend.services.option_lookup import get_tradier_option_symbol

logger = logging.getLogger(__name__)

from backend.services.tradier_client import TradierClient

async def build_order(ticker: str, contracts: int, dte: int, mode: str) -> dict:
    return {
        "class": "equity",
        "symbol": ticker,
        "side": "buy",
        "quantity": contracts,
        "price": None
    }