from typing import Dict, Any
from datetime import date, timedelta
from backend.services.tradier_client import TradierClient
from backend.services.rounding_util import round_to_increment
from backend.services.option_lookup import get_tradier_option_symbol

async def build_order(ticker: str, contracts: int = 1, dte: int = 1, mode: str = "sandbox") -> Dict[str, Any]:
    from typing import Dict, Any
    import logging
    import logging
    from datetime import date, timedelta
    from backend.services.tradier_client import TradierClient
    from backend.services.option_lookup import get_tradier_option_symbol
    logger = logging.getLogger(__name__)
    # backend/bots/momentumbot.py
    from backend.services.rounding_util import round_to_increment
    from backend.services.option_lookup    import get_tradier_option_symbol
    from backend.services.option_lookup import get_tradier_option_symbol
    from backend.services.tradier_client import TradierClient
    expiration = (date.today() + timedelta(days=dte)).strftime("%Y-%m-%d")
    # Fetch current quote
    client = TradierClient()
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

    return {
        "legs": [],
        "price": None,
        "order_type": "market",
        "duration": "day",
        "tag": "momentumbot"
    }
