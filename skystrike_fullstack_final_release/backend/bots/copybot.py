import logging
# backend/bots/copybot.py

from backend.services.rounding_util import round_to_increment
from backend.services.option_lookup    import get_tradier_option_symbol
from typing import Dict, Any
from datetime import date, timedelta
from backend.services.option_lookup import get_tradier_option_symbol
from backend.services.tradier_client import TradierClient

logger = logging.getLogger(__name__)

async def build_order(ticker: str, contracts: int, dte: int, mode: str) -> Dict[str, Any]:
    """
    CopyBot: Example bull put spread structure that mimics another strategy.
    Uses live Tradier option chain to resolve valid symbols.
    """

    expiration = (date.today() + timedelta(days=dte)).strftime("%Y-%m-%d")

    # Use live market data to anchor strike selection
    client = TradierClient(sandbox=(mode == "paper"))
    quote = client.get_quote(ticker)
    price = float(quote.get("last", 100))

    short_strike = round_to_increment(price * 0.93, 0.5)
    long_strike = short_strike - 5

    # Resolve option symbols via Tradier API
    short_put = get_tradier_option_symbol(ticker, expiration, short_strike, "put")
    long_put  = get_tradier_option_symbol(ticker, expiration, long_strike, "put")

    legs = [
        {"option_symbol": short_put, "side": "sell", "quantity": contracts},
        {"option_symbol": long_put,  "side": "buy",  "quantity": contracts}
    ]

    logger.info(f"[COPYBOT] {ticker} PUT spread {short_strike}/{long_strike} exp {expiration} x{contracts}")

    return {
        "legs": legs,
        "price": 1.0
    }
