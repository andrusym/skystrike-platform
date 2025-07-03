from backend.services.tradier_client import TradierClient
import logging
# backend/bots/trend.py

from backend.services.rounding_util import round_to_increment
from backend.services.option_lookup    import get_tradier_option_symbol
from typing import Dict, Any
from datetime import date, timedelta

from backend.bots.base import TradierClient
from backend.services.option_lookup import get_tradier_option_symbol

logger = logging.getLogger(__name__)

async def build_order(
    ticker: str,
    contracts: int,
    dte: int,
    mode: str
) -> Dict[str, Any]:
    """
    TrendBot: Builds a directional put spread to capture trend continuation
    in bearish regimes. Adjust strike deeper if price is falling.
    """

    # Determine expiration date (YYYY-MM-DD)
    expiration = (date.today() + timedelta(days=dte)).strftime("%Y-%m-%d")

    # Fetch latest quote
    client = TradierClient(sandbox=(mode == "paper"))
    quote = client.get_quote(ticker)
    price = float(quote.get("last", 0))

    # Momentum logic: go deeper if price is falling
    short_strike = round_to_increment(price * 0.92, 0.5)
    long_strike  = short_strike - 5

    # Build OCC-compliant option symbols (with automatic fallback)
    short_put = get_tradier_option_symbol(ticker, expiration, short_strike, "put")
    long_put  = get_tradier_option_symbol(ticker, expiration, long_strike,  "put")

    legs = [
        {"option_symbol": short_put, "side": "sell_to_open", "quantity": contracts},
        {"option_symbol": long_put,  "side": "buy_to_open",  "quantity": contracts},
    ]

    logger.info(
        f"[TREND] {ticker} PUT spread {short_strike}/{long_strike} "
        f"exp {expiration} x{contracts}"
    )

    return {
        "legs": legs,
        "price": 1.0,
    }
