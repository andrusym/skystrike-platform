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
    # backend/bots/wheel.py
    from backend.services.rounding_util import round_to_increment
    from backend.services.option_lookup    import get_tradier_option_symbol
    from backend.services.option_lookup import get_tradier_option_symbol
    from backend.services.tradier_client import TradierClient
    expiration = (date.today() + timedelta(days=dte)).strftime("%Y-%m-%d")
    # Fetch live quote
    client = TradierClient()
    quote = client.get_quote(ticker)
    price = float(quote.get("last", 100))
    # Slightly OTM entry (90% of spot)
    strike = round_to_increment(price * 0.90, 0.5)
    option_symbol = get_tradier_option_symbol(ticker, expiration, strike, "put")
    logger.info(f"[WHEEL] {ticker} selling PUT {strike} exp {expiration} x{contracts}")
    return {
    "option_symbol": option_symbol,
    "side": "sell",
    "quantity": contracts,
    "price": 1.0
    }

    return {
        "legs": [],
        "price": None,
        "order_type": "market",
        "duration": "day",
        "tag": "wheel"
    }
