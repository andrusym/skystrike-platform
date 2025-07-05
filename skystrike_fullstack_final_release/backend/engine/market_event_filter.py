# backend/engine/market_event_filter.py

import logging
from datetime import date

logger = logging.getLogger(__name__)

# Predefined dates on which to skip trading (macro risk events)
MACRO_RISK_DATES = [
    # e.g. "2025-07-31", "2025-09-17"
]

def should_skip_today() -> bool:
    """
    Determine whether to skip trading today due to macro risk events.
    Returns True if today's date is in the MACRO_RISK_DATES list.
    Extend by adding dates or integrating with an external calendar API.
    """
    today_str = date.today().isoformat()
    if today_str in MACRO_RISK_DATES:
        logger.info(f"Skipping trading for macro risk event on {today_str}")
        return True
    return False

__all__ = ["should_skip_today"]
