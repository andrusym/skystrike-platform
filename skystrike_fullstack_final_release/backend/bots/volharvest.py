from backend.services.tradier_client import TradierClient
import logging
from backend.services.rounding_util import round_to_increment
from backend.services.option_lookup    import get_tradier_option_symbol
from backend.services.rounding_util import round_to_increment
from backend.services.option_lookup    import get_tradier_option_symbol
from typing import Dict, Any
from datetime import date, timedelta

logger = logging.getLogger(__name__)

async def build_order(ticker: str, contracts: int, dte: int, mode: str) -> Dict[str, Any]:
    """
    Enter iron condors or butterflies post-event to harvest IV crush.
    """

    expiration = (date.today() + timedelta(days=dte)).strftime("%Y-%m-%d")
    expiry_code = expiration.replace("-", "")

    client = TradierClient(sandbox=(mode == "paper"))
    quote = client.get_quote(ticker)
    price = float(quote.get("last", 100))

    # Example logic (customize per bot)
    short_strike = round_to_increment(price * 0.95, 0.5)
    long_strike  = short_strike - 5

    short_opt = client.format_option(ticker, expiry_code, "P", short_strike)
    long_opt  = client.format_option(ticker, expiry_code, "P", long_strike)

    legs = [
        {"option_symbol": short_opt, "side": "sell_to_open", "quantity": contracts},
        {"option_symbol": long_opt,  "side": "buy_to_open",  "quantity": contracts}
    ]

    logger.info(f"[VOLHARVEST] {ticker} spread {short_strike}/{long_strike} exp {expiration} x{contracts}")

    return {
        "legs": legs,
        "price": 1.0
    }
