
import logging
from typing import Dict, Any
from datetime import date, timedelta
from backend.services.tradier_client import TradierClient
from backend.services.option_lookup import get_tradier_option_symbol

logger = logging.getLogger(__name__)

# backend/bots/scalper.py

from backend.services.rounding_util import round_to_increment
from backend.services.option_lookup    import get_tradier_option_symbol


from backend.services.option_lookup import get_tradier_option_symbol
from backend.services.tradier_client import TradierClient



async def build_order(ticker: str, contracts: int, dte: int, mode: str) -> Dict[str, Any]:
    """
    ScalperBot: Builds a tight delta-neutral put spread to capture short-term premium.
    Designed for high turnover with fast entry/exit logic.
    """

    expiration = (date.today() + timedelta(days=dte)).strftime("%Y-%m-%d")

    # Get live market price
    client = TradierClient(mode=mode)
    quote = await client.get_quote(ticker)
    price = float(quote.get("last", 100))

    # Narrow OTM spread: ~96% of price
    short_strike = round_to_increment(price * 0.96, 0.5)
    long_strike = short_strike - 2

    # Lookup valid Tradier option symbols
    short_put = await get_tradier_option_symbol(ticker, expiration, short_strike, "put")
    long_put  = await get_tradier_option_symbol(ticker, expiration, long_strike, "put")

    legs = [
        {"option_symbol": short_put, "side": "sell", "quantity": contracts},
        {"option_symbol": long_put,  "side": "buy",  "quantity": contracts}
    ]

    logger.info(f"[SCALPER] {ticker} PUT spread {short_strike}/{long_strike} exp {expiration} x{contracts}")

    return {
        "legs": legs,
        "price": 1.0
    }