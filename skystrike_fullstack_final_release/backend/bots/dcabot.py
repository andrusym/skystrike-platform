import logging
# backend/bots/dcabot.py

from backend.services.rounding_util import round_to_increment
from backend.services.option_lookup    import get_tradier_option_symbol
from typing import Dict, Any
from datetime import date, timedelta
from backend.services.option_lookup import get_tradier_option_symbol
from backend.services.tradier_client import TradierClient

logger = logging.getLogger(__name__)

async def build_order(ticker: str, contracts: int, dte: int, mode: str) -> Dict[str, Any]:
    """
    Build a dollar-cost averaging (DCA) entry via short put spread.
    This approach simulates phased entry by selling a put spread
    near support.
    """

    expiration = (date.today() + timedelta(days=dte)).strftime("%Y-%m-%d")

    # Fetch current market price
    client = TradierClient(sandbox=(mode == "paper"))
    quote = client.get_quote(ticker)
    last_price = float(quote.get("last", 100))

    # Strike logic: ~92% of current price
    short_strike = round_to_increment(last_price * 0.92, 0.5)
    long_strike  = short_strike - 5

    # Get Tradier-compliant option symbols
    short_put = get_tradier_option_symbol(ticker, expiration, short_strike, "put")
    long_put  = get_tradier_option_symbol(ticker, expiration, long_strike, "put")

    legs = [
        {"option_symbol": short_put, "side": "sell", "quantity": contracts},
        {"option_symbol": long_put,  "side": "buy",  "quantity": contracts}
    ]

    logger.info(f"[DCABOT] {ticker} PUT spread {short_strike}/{long_strike} exp {expiration} x{contracts}")

    return {
        "legs": legs,
        "price": 1.0
    }
