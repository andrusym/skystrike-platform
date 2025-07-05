# backend/engine/quote_stream_engine.py

"""
Quote Stream Engine: supports real-time quote tracking for given tickers.
"""

import logging
import time
from typing import List, Callable
from backend.services.tradier_api import get_quote

logger = logging.getLogger(__name__)

def start_streaming_quotes(
    tickers: List[str],
    on_quote: Callable[[str, float], None],
    interval_secs: int = 60
) -> None:
    """
    Start a simple polling-based quote stream.
    Calls `on_quote(ticker, price)` for each ticker every `interval_secs`.
    Replace with websocket or streaming API integration as needed.
    """
    logger.info(f"Starting quote stream for: {tickers}, interval: {interval_secs}s")
    while True:
        for ticker in tickers:
            try:
                quote = get_quote(ticker)
                price = quote.get("last", quote.get("last_quote", quote.get("last_price", 0.0)))
                logger.debug(f"Quote for {ticker}: {price}")
                on_quote(ticker, price)
            except Exception as e:
                logger.warning(f"Failed to fetch quote for {ticker}: {e}")
        time.sleep(interval_secs)

__all__ = ["start_streaming_quotes"]
