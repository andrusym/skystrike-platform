import logging
from typing import Dict, Any
from datetime import date, timedelta

from backend.services.rounding_util import round_to_increment
from backend.services.option_lookup import get_tradier_option_symbol
from backend.services.tradier_client import TradierClient

logger = logging.getLogger(__name__)

async def build_order(
    ticker: str,
    contracts: int,
    dte: int,
    mode: str
) -> Dict[str, Any]:
    """
    Build a 4-leg Iron Condor using +/-5 and +/-10 strikes around ATM.
    Constructs two credit spreads: short put spread + short call spread.
    """
    # Determine expiration
    expiration = (date.today() + timedelta(days=dte)).strftime("%Y-%m-%d")

    # Fetch market quote
    client = TradierClient(sandbox=(mode == "paper"))
    quote = client.get_quote(ticker)
    last_price = float(quote.get("last", 100))
    atm_strike = round_to_increment(last_price, 0.5)

    # Define strike legs
    put_short_strike = atm_strike - 5
    put_long_strike  = atm_strike - 10
    call_short_strike = atm_strike + 5
    call_long_strike  = atm_strike + 10

    # Lookup Tradier-compliant option symbols
    put_short  = get_tradier_option_symbol(ticker, expiration, put_short_strike, "put")
    put_long   = get_tradier_option_symbol(ticker, expiration, put_long_strike, "put")
    call_short = get_tradier_option_symbol(ticker, expiration, call_short_strike, "call")
    call_long  = get_tradier_option_symbol(ticker, expiration, call_long_strike, "call")

    legs = [
        {"option_symbol": put_short,  "side": "sell", "quantity": contracts},
        {"option_symbol": put_long,   "side": "buy",  "quantity": contracts},
        {"option_symbol": call_short, "side": "sell", "quantity": contracts},
        {"option_symbol": call_long,  "side": "buy",  "quantity": contracts},
    ]

    logger.info(f"[IRON CONDOR] {ticker} ATM {atm_strike} exp {expiration} x{contracts}")
    return {
        "legs": legs,
        "price": 1.0
    }
