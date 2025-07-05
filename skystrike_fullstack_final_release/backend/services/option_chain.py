import logging
from datetime import datetime
from backend.services.tradier_client import TradierClient
from backend.services.rounding_util import get_nearest_strike

logger = logging.getLogger(__name__)


def format_option_symbol(ticker: str, date_str: str, callput: str, strike: float) -> str:
    """
    Build an OCC-compliant option symbol: TICKER + YYMMDD + P/C + zero-padded strike.
    """
    date_fmt = datetime.strptime(date_str, "%Y-%m-%d").strftime("%y%m%d")
    letter = "P" if callput.lower().startswith("p") else "C"
    strike_fmt = f"{int(strike * 1000):08d}"
    return f"{ticker.upper()}{date_fmt}{letter}{strike_fmt}"


def get_tradier_option_symbol(
    ticker: str,
    expiration: str,
    requested_strike: float,
    callput: str
) -> str:
    """
    Fetch Tradier OCC option symbol using the nearest available strike.
    Falls back to nearest expiration if necessary.
    """
    client = TradierClient()

    def fetch_strikes(exp: str):
        chain = client.get_option_chain(ticker, exp)
        if not chain:
            return []
        return sorted({
            float(opt["strike"])
            for opt in chain
            if opt.get("option_type", "").lower() == callput.lower()
        })

    # Step 1: Try initial expiration
    strikes = fetch_strikes(expiration)

    # Step 2: Fallback if no options
    if not strikes:
        expirations = client.get_expirations(ticker)
        if not expirations:
            raise ValueError(f"No expirations available for {ticker}")
        dates = [datetime.strptime(d, "%Y-%m-%d").date() for d in expirations]
        req_date = datetime.strptime(expiration, "%Y-%m-%d").date()
        nearest_date = min(dates, key=lambda d: abs((d - req_date).days))
        new_exp = nearest_date.strftime("%Y-%m-%d")
        logger.warning(
            f"No {callput.upper()} options for {ticker} on {expiration}; "
            f"falling back to expiration {new_exp}"
        )
        expiration = new_exp
        strikes = fetch_strikes(expiration)
        if not strikes:
            raise ValueError(
                f"No {callput.upper()} options at all for {ticker} after fallback to {expiration}"
            )

    # Step 3: Choose nearest valid strike
    if requested_strike not in strikes:
        nearest = get_nearest_strike(strikes, requested_strike)
        logger.warning(
            f"{ticker} {expiration} {callput.upper()} strike {requested_strike} not found - using nearest {nearest}"
        )
        strike = nearest
    else:
        strike = requested_strike

    return format_option_symbol(ticker, expiration, callput, strike)
