import time
import logging
from backend.services.tradier_client import TradierClient

logger = logging.getLogger(__name__)
_tradier = TradierClient()

class SmartEntryRetry:
    def __init__(self, max_attempts: int = 3, delay_seconds: int = 5):
        self.max_attempts = max_attempts
        self.delay_seconds = delay_seconds

    def try_execute(self, trade: dict) -> dict:
        for attempt in range(1, self.max_attempts + 1):
            try:
                result = _tradier.place_order(**trade)
                logger.info(f"[SmartEntryRetry] Success on attempt {attempt}")
                return result
            except Exception as e:
                logger.warning(f"[SmartEntryRetry] Attempt {attempt} failed: {e}")
                time.sleep(self.delay_seconds)
        raise RuntimeError("All retry attempts failed for trade execution.")
