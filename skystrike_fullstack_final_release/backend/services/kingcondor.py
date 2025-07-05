from typing import Dict, Any
import logging
from datetime import date, timedelta

from backend.services.tradier_client import TradierClient
from backend.services.rounding_util import round_to_increment
from backend.services.option_lookup import get_tradier_option_symbol

logger = logging.getLogger(__name__)

async def build_order(ticker: str, contracts: int = 1, dte: int = 1, mode: str = "sandbox") -> Dict[str, Any]:
    """
    Build a wider Iron Condor with custom wings for high volatility regimes.
    """
    expiration = (date.today() + timedelta(days=dte)).strftime("%Y-%m-%d")

    client = TradierClient(mode=mode)
    quote = client.get_quote(ticker)
    price = float(quote.get("last", 100))

    spread = 10
    put_short = round_to_increment(price * 0.93, 1.0)
    put_long = put_short - spread
    call_short = round_to_increment(price * 1.07, 1.0)
    call_long = call_short + spread

    legs = [
        {
            "option_symbol": get_tradier_option_symbol(ticker, expiration, put_short, "put"),
            "side": "sell_to_open",
            "quantity": contracts
        },
        {
            "option_symbol": get_tradier_option_symbol(ticker, expiration, put_long, "put"),
            "side": "buy_to_open",
            "quantity": contracts
        },
        {
            "option_symbol": get_tradier_option_symbol(ticker, expiration, call_short, "call"),
            "side": "sell_to_open",
            "quantity": contracts
        },
        {
            "option_symbol": get_tradier_option_symbol(ticker, expiration, call_long, "call"),
            "side": "buy_to_open",
            "quantity": contracts
        }
    ]

    return {
        "legs": legs,
        "price": None,
        "order_type": "market",
        "duration": "day",
        "tag": "kingcondor"
    }
