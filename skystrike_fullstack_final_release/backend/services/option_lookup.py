import logging
from datetime import datetime
from typing import Optional
from backend.services.tradier_client import TradierClient
from backend.services.rounding_util import get_nearest_strike

logger = logging.getLogger(__name__)

def format_option_symbol(ticker: str, date_str: str, callput: str, strike: float) -> str:
    date_fmt = datetime.strptime(date_str, "%Y-%m-%d").strftime("%y%m%d")
    letter = "P" if callput.lower().startswith("p") else "C"
    strike_fmt = f"{int(strike * 1000):08d}"
    return f"{ticker.upper()}{date_fmt}{letter}{strike_fmt}"

async def get_tradier_option_symbol(
    ticker: str,
    expiration: str,
    requested_strike: float,
    callput: str,
    mode: str = "paper"
) -> str:
    client = TradierClient(mode=mode)

    async def fetch_strikes(exp: str):
        chain = await client.get_option_chain(ticker, exp)
        opts = chain.get("options", [])
        return sorted({
            float(o["strike"])
            for o in opts
            if o.get("option_type", "").lower() == callput.lower()
        })

    strikes = await fetch_strikes(expiration)

    if not strikes:
        expirations = await client.get_expirations(ticker)
        dates = [datetime.strptime(d, "%Y-%m-%d").date() for d in expirations]
        req_date = datetime.strptime(expiration, "%Y-%m-%d").date()
        nearest_date = min(dates, key=lambda d: abs((d - req_date).days))
        new_exp = nearest_date.strftime("%Y-%m-%d")
        logger.warning(f"No {callput.upper()} options for {ticker} on {expiration}; falling back to {new_exp}")
        expiration = new_exp
        strikes = await fetch_strikes(expiration)
        if not strikes:
            raise ValueError(f"No {callput.upper()} options at all for {ticker} after fallback to {expiration}")

    if requested_strike not in strikes:
        nearest = get_nearest_strike(strikes, requested_strike)
        logger.warning(f"{ticker} {expiration} {callput.upper()} strike {requested_strike} not found - using nearest {nearest}")
        strike = nearest
    else:
        strike = requested_strike

    return format_option_symbol(ticker, expiration, callput, strike)
