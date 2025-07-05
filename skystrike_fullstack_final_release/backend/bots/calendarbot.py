from typing import Dict, Any

import logging
from datetime import date, timedelta

from backend.services.tradier_client import TradierClient
from backend.services.option_lookup import get_tradier_option_symbol
from backend.services.rounding_util import round_to_increment

logger = logging.getLogger(__name__)

async def build_order(ticker: str, contracts: int = 1, dte: int = 30, mode: str = "sandbox") -> Dict[str, Any]:
    """
    Construct a basic calendar spread.
    """
    near_expiration = (date.today() + timedelta(days=7)).strftime("%Y-%m-%d")
    far_expiration  = (date.today() + timedelta(days=dte)).strftime("%Y-%m-%d")
    expiry_near = near_expiration.replace("-", "")
    expiry_far  = far_expiration.replace("-", "")

    client = TradierClient(mode=mode)
    quote = await client.get_quote(ticker)
    price = float(quote.get("last", 100))
    strike = round_to_increment(price, 1.0)

    opt_short = client.format_option(ticker, expiry_near, "C", strike)
    opt_long  = client.format_option(ticker, expiry_far,  "C", strike)

    legs = [
        {"option_symbol": opt_short, "side": "sell_to_open", "quantity": contracts},
        {"option_symbol": opt_long,  "side": "buy_to_open",  "quantity": contracts}
    ]

    logger.info(f"[CALENDBOT] {ticker} calendar {strike} exp {near_expiration}/{far_expiration} x{contracts}")

    return {
        "legs": legs,
        "price": 1.0
    }
