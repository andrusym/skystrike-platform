from typing import Dict, Any

import logging
from datetime import date, timedelta

from backend.services.tradier_client import TradierClient
from backend.services.option_lookup import get_tradier_option_symbol
from backend.services.rounding_util import round_to_increment

logger = logging.getLogger(__name__)

async def build_order(ticker: str, contracts: int = 1, dte: int = 1, mode: str = "sandbox") -> Dict[str, Any]:
    """
    Construct a bull put spread when price breaks support.
    """
    expiration = (date.today() + timedelta(days=dte)).strftime("%Y-%m-%d")
    expiry_code = expiration.replace("-", "")

    client = TradierClient(mode=mode)
    quote = await client.get_quote(ticker)
    price = float(quote.get("last", 100))

    short_strike = round_to_increment(price * 0.95, 0.5)
    long_strike  = short_strike - 5

    short_opt = client.format_option(ticker, expiry_code, "P", short_strike)
    long_opt  = client.format_option(ticker, expiry_code, "P", long_strike)

    legs = [
        {"option_symbol": short_opt, "side": "sell_to_open", "quantity": contracts},
        {"option_symbol": long_opt,  "side": "buy_to_open",  "quantity": contracts}
    ]

    logger.info(f"[BREAKOUTBOT] {ticker} spread {short_strike}/{long_strike} exp {expiration} x{contracts}")

    return {
        "legs": legs,
        "price": 1.0
    }
