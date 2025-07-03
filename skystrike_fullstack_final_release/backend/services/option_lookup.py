import logging
from datetime import datetime
from backend.services.tradier_client import TradierClient
from backend.services.rounding_util import get_nearest_strike

logger = logging.getLogger(__name__)

def format_option_symbol(ticker: str, date_str: str, callput: str, strike: float) -> str:
    """
    Build an OCC-compliant option symbol: TICKER + YYMMDD + P/C + zero-padded strike.
    """
    # expiration date as YYMMDD
    date_fmt = datetime.strptime(date_str, "%Y-%m-%d").strftime("%y%m%d")
    # choose single-letter right code
    letter = "P" if callput.lower().startswith("p") else "C"
    # strike * 1000, padded to 8 digits
    strike_fmt = f"{int(strike * 1000):08d}"
    return f"{ticker.upper()}{date_fmt}{letter}{strike_fmt}"


def get_tradier_option_symbol(
    ticker: str,
    expiration: str,
    requested_strike: float,
    callput: str
) -> str:
    """
    Fetch the option chain for `ticker` expiring on `expiration`.
    If there are no options of type `callput`, fall back to the nearest expiration.
    Then return the OCC symbol for the exact `requested_strike` if present,
    otherwise fall back to the nearest available strike.
    Raises ValueError only if truly no options exist after expiration fallback.
    """
    client = TradierClient(sandbox=True)

    def fetch_strikes(exp: str):
        chain = client.get_option_chain(ticker, exp)
        opts = chain.get("options", [])
        return sorted({
            float(o["strike"])
            for o in opts
            if o.get("option_type", "").lower() == callput.lower()
        })

    # 1) Try the requested expiration
    strikes = fetch_strikes(expiration)

    # 2) If none, fall back to nearest expiration date
    if not strikes:
        expirations = client.get_expirations(ticker)  # list of "YYYY-MM-DD"
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
                f"No {callput.upper()} options at all for {ticker} "
                f"after falling back to {expiration}"
            )

    # 3) Pick exact or nearest strike using rounding_util
    if requested_strike not in strikes:
        nearest = get_nearest_strike(strikes, requested_strike)
        logger.warning(
            f"{ticker} {expiration} {callput.upper()} strike {requested_strike} "
            f"not found - using nearest {nearest}"
        )
        strike = nearest
    else:
        strike = requested_strike

    return format_option_symbol(ticker, expiration, callput, strike)
