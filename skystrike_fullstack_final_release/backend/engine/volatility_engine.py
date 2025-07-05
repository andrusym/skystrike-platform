# backend/engine/volatility_engine.py

"""
Volatility Engine: fetches current VIX level and classifies regime.
"""

import logging

logger = logging.getLogger(__name__)

def get_vix_level() -> float:
    """
    Fetch the latest VIX close price using yfinance.
    """
    try:
        import yfinance as yf
    except ImportError:
        msg = (
            "Missing dependency 'yfinance'.\n"
            "Install it with: pip install yfinance"
        )
        logger.error(msg)
        raise ImportError(msg)

    try:
        vix = yf.Ticker("^VIX")
        hist = vix.history(period="1d")
        if hist.empty:
            raise ValueError("No VIX data available")
        return float(hist["Close"].iloc[-1])
    except Exception as e:
        logger.warning(f"VIX fetch failed: {e}. Using default VIX=20.0")
        return 20.0

def classify_volatility_regime(vix: float) -> str:
    """
    Classify volatility regime based on VIX value.
    """
    if vix < 15:
        return "low"
    elif vix < 25:
        return "moderate"
    elif vix < 35:
        return "high"
    else:
        return "extreme"

__all__ = ["get_vix_level", "classify_volatility_regime"]
