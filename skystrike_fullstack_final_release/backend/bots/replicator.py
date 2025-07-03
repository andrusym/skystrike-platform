from backend.services.tradier_client import TradierClient
import logging
# backend/bots/replicator.py

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
    Replicator: Builds a short put spread to replicate the entry of a larger signal engine.
    Typically used to shadow trades across models or accounts.
    """

    # Determine expiration date (YYYY-MM-DD)
    expiration = (date.today() + timedelta(days=dte)).strftime("%Y-%m-%d")

    # Fetch live quote
    client = TradierClient(sandbox=(mode == "paper"))
    quote = client.get_quote(ticker)
    last_price = float(quote.get("last", 0))

    # Replicate logic: 95% of underlying
    short_strike = round_to_increment(last_price * 0.95, 0.5)
    long_strike  = short_strike - 5

    # Build OCC-compliant option symbols (with automatic fallback to nearest strike/expiry)
    short_put = get_tradier_option_symbol(ticker, expiration, short_strike, "put")
    long_put  = get_tradier_option_symbol(ticker, expiration, long_strike,  "put")

    legs = [
        {"option_symbol": short_put, "side": "sell_to_open", "quantity": contracts},
        {"option_symbol": long_put,  "side": "buy_to_open",  "quantity": contracts},
    ]

    logger.info(
        f"[REPLICATOR] {ticker} PUT spread {short_strike}/{long_strike} "
        f"exp {expiration} x{contracts}"
    )

    return {
        "legs": legs,
        "price": 1.0,
    }
