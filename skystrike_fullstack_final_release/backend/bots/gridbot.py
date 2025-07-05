import logging
from typing import Dict, Any
from datetime import date, timedelta

from backend.services.tradier_client import TradierClient
from backend.services.option_lookup import get_tradier_option_symbol
from backend.services.rounding_util import round_to_increment

logger = logging.getLogger(__name__)

async def build_order(ticker: str, contracts: int, dte: int, mode: str) -> Dict[str, Any]:
    """
    GridBot: Constructs a wide short put spread (deep OTM) to scale into volatility dips.
    """

    expiration = (date.today() + timedelta(days=dte)).strftime("%Y-%m-%d")

    # Fetch latest market quote
    client = TradierClient(mode=mode)
    quote = await client.get_quote(ticker)
    last_price = float(quote.get("last", 100))

    # Deep OTM spread target (88% of price)
    short_strike = round_to_increment(last_price * 0.88, 0.5)
    long_strike  = short_strike - 5

    # Resolve real Tradier option symbols
    short_put = await get_tradier_option_symbol(ticker, expiration, short_strike, "put")
    long_put  = await get_tradier_option_symbol(ticker, expiration, long_strike, "put")

    legs = [
        {"option_symbol": short_put, "side": "sell", "quantity": contracts},
        {"option_symbol": long_put,  "side": "buy",  "quantity": contracts}
    ]

    logger.info(f"[GRIDBOT] {ticker} PUT spread {short_strike}/{long_strike} exp {expiration} x{contracts}")

    return {
        "legs": legs,
        "price": 1.0,
        "order_type": "market",
        "duration": "day",
        "tag": "gridbot"
    }
