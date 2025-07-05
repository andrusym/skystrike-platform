# backend/engine/dynamic_dte_selector.py

import logging
from datetime import date, timedelta
from backend.services.tradier_api import TradierClient

logger = logging.getLogger(__name__)


def get_vix_level() -> float:
    """
    Fetch the latest VIX index level from Tradier.
    Returns None if unavailable.
    """
    try:
        client = TradierClient()
        quote = client.get_quote("VIX")
        return float(quote.get("last"))
    except Exception as e:
        logger.warning(f"[get_vix_level] Failed to fetch VIX quote: {e}")
        return None


def choose_optimal_dte(ticker: str) -> date:
    """
    Selects an optimal expiration date for options based on historical volatility.
    Requires 'yfinance' library. If not installed, raises ImportError with instructions.
    """
    try:
        import yfinance as yf
    except ImportError:
        msg = (
            "Missing dependency 'yfinance'.\n"
            "Install it with: pip install yfinance\n"
            "Then restart your application."
        )
        logger.error(msg)
        raise ImportError(msg)

    # Attempt to fetch recent data for volatility calculation
    try:
        ticker_obj = yf.Ticker(ticker)
        hist = ticker_obj.history(period="5d")
        if hist.empty:
            raise ValueError(f"No historical data for ticker: {ticker}")
        # Annualized volatility estimation
        returns = hist['Close'].pct_change().dropna()
        vol = returns.std() * (252 ** 0.5)
    except Exception as e:
        logger.warning(f"Volatility fetch failed for {ticker}: {e}. Using default DTE=1.")
        return _next_business_day(1)

    # Simple rule: high vol -> 0 DTE, else -> 1 DTE
    threshold = 0.02  # ~2% annual vol
    dte_days = 0 if vol > threshold else 1
    return _next_business_day(dte_days)


def _next_business_day(offset_days: int) -> date:
    """
    Returns the date of the next business day offset from today.
    offset_days=0 -> next available business day
    offset_days=1 -> the business day after that, etc.
    """
    d = date.today()
    days_to_skip = offset_days
    while days_to_skip >= 0:
        d += timedelta(days=1)
        if d.weekday() < 5:  # Mon-Fri
            days_to_skip -= 1
    return d
