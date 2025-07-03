import logging
# backend/bots/momentumbot.py

from backend.services.rounding_util import round_to_increment
from backend.services.option_lookup    import get_tradier_option_symbol
from typing import Dict, Any
from datetime import date, timedelta
from backend.services.option_lookup import get_tradier_option_symbol
from backend.services.tradier_client import TradierClient

logger = logging.getLogger(__name__)

async def build_order(ticker: str, contracts: int, dte: int, mode: str) -> Dict[str, Any]:
    """
    MomentumBot: Builds a bearish put spread on breakdowns.
    Targets momentum plays where IV expansion + trend continuation is likely.
    """

    expiration = (date.today() + timedelta(days=dte)).strftime("%Y-%m-%d")

    # Fetch current quote
    client = TradierClient(sandbox=(mode == "paper"))
    quote = client.get_quote(ticker)
    price = float(quote.get("last", 100))

    # Strategy: Sell slightly below price, buy deeper
    short_strike = round_to_increment(price * 0.97, 0.5)
    long_strike  = short_strike - 5

    # Resolve symbols from Tradier chain
    short_put = get_tradier_option_symbol(ticker, expiration, short_strike, "put")
    long_put  = get_tradier_option_symbol(ticker, expiration, long_strike, "put")

    legs = [
        {"option_symbol": short_put, "side": "sell", "quantity": contracts},
        {"option_symbol": long_put,  "side": "buy",  "quantity": contracts}
    ]

    logger.info(f"[MOMENTUM] {ticker} PUT spread {short_strike}/{long_strike} exp {expiration} x{contracts}")

    return {
        "legs": legs,
        "price": 1.0
    }
