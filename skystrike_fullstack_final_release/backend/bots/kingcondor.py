import logging
# backend/bots/kingcondor.py

from backend.services.rounding_util import round_to_increment
from backend.services.option_lookup    import get_tradier_option_symbol
from typing import Dict, Any
from datetime import date, timedelta
from backend.services.option_lookup import get_tradier_option_symbol
from backend.services.tradier_client import TradierClient

logger = logging.getLogger(__name__)

async def build_order(ticker: str, contracts: int, dte: int, mode: str) -> Dict[str, Any]:
    """
    King Condor: Wider wingspan iron condor targeting IV expansion.
    Ideal for higher premium capture in low gamma regimes.
    """

    expiration = (date.today() + timedelta(days=dte)).strftime("%Y-%m-%d")

    # Fetch underlying price
    client = TradierClient(sandbox=(mode == "paper"))
    quote = client.get_quote(ticker)
    last_price = float(quote.get("last", 100))
    atm_strike = round_to_increment(last_price, 0.5)

    # Build a 10/20-point wingspan iron condor
    put_short_strike  = atm_strike - 10
    put_long_strike   = atm_strike - 20
    call_short_strike = atm_strike + 10
    call_long_strike  = atm_strike + 20

    # Fetch valid Tradier option symbols
    put_short  = get_tradier_option_symbol(ticker, expiration, put_short_strike, "put")
    put_long   = get_tradier_option_symbol(ticker, expiration, put_long_strike, "put")
    call_short = get_tradier_option_symbol(ticker, expiration, call_short_strike, "call")
    call_long  = get_tradier_option_symbol(ticker, expiration, call_long_strike, "call")

    legs = [
        {"option_symbol": put_short,  "side": "sell", "quantity": contracts},
        {"option_symbol": put_long,   "side": "buy",  "quantity": contracts},
        {"option_symbol": call_short, "side": "sell", "quantity": contracts},
        {"option_symbol": call_long,  "side": "buy",  "quantity": contracts}
    ]

    logger.info(f"[KING CONDOR] {ticker} wide condor {atm_strike}-10/20 exp {expiration} x{contracts}")

    return {
        "legs": legs,
        "price": 1.0
    }
