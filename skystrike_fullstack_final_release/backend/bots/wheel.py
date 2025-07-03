import logging
# backend/bots/wheel.py

from backend.services.rounding_util import round_to_increment
from backend.services.option_lookup    import get_tradier_option_symbol
from typing import Dict, Any
from datetime import date, timedelta
from backend.services.option_lookup import get_tradier_option_symbol
from backend.services.tradier_client import TradierClient

logger = logging.getLogger(__name__)

async def build_order(ticker: str, contracts: int, dte: int, mode: str) -> Dict[str, Any]:
    """
    WheelBot: Opens a naked cash-secured put to initiate the wheel strategy.
    No long leg is included (not a spread).
    """

    expiration = (date.today() + timedelta(days=dte)).strftime("%Y-%m-%d")

    # Fetch live quote
    client = TradierClient(sandbox=(mode == "paper"))
    quote = client.get_quote(ticker)
    price = float(quote.get("last", 100))

    # Slightly OTM entry (90% of spot)
    strike = round_to_increment(price * 0.90, 0.5)
    option_symbol = get_tradier_option_symbol(ticker, expiration, strike, "put")

    logger.info(f"[WHEEL] {ticker} selling PUT {strike} exp {expiration} x{contracts}")

    return {
        "option_symbol": option_symbol,
        "side": "sell",
        "quantity": contracts,
        "price": 1.0
    }
