
import logging
from typing import Dict, Any
from datetime import date, timedelta
from backend.services.tradier_client import TradierClient
from backend.services.option_lookup import get_tradier_option_symbol

logger = logging.getLogger(__name__)

# backend/bots/csp.py

from backend.services.rounding_util import round_to_increment
from backend.services.option_lookup    import get_tradier_option_symbol


from backend.services.option_lookup import get_tradier_option_symbol
from backend.services.tradier_client import TradierClient



async def build_order(ticker: str, contracts: int, dte: int, mode: str) -> Dict[str, Any]:
    """
    Build a simple cash-secured put structure.
    This implementation sells a single put contract at-the-money.
    """

    expiration = (date.today() + timedelta(days=dte)).strftime("%Y-%m-%d")

    # Fetch underlying quote
    client = TradierClient(mode=mode)
    quote = await client.get_quote(ticker)
    underlying_price = float(quote.get("last", 100))
    strike = round_to_increment(underlying_price, 0.5)

    # Get real option symbol via Tradier API
    option_symbol = await get_tradier_option_symbol(ticker, expiration, strike, "put")

    logger.info(f"[CSP] {ticker} ATM PUT {strike} exp {expiration} x{contracts}")

    return {
        "option_symbol": option_symbol,
        "side": "sell",
        "quantity": contracts,
        "price": 1.0
    }