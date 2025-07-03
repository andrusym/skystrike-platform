
# smart_entry_retry.py

import time
import logging
utils.broker_api import execute_trade

class SmartEntryRetry:
    def __init__(self, max_attempts=3, delay_seconds=5):
        self.max_attempts = max_attempts
        self.delay_seconds = delay_seconds

    def try_execute(self, trade):
        for attempt in range(1, self.max_attempts + 1):
            try:
                result = execute_trade(trade)
                logging.info(f"[SmartEntryRetry] Success on attempt {attempt}")
                return result
            except Exception as e:
                logging.warning(f"[SmartEntryRetry] Attempt {attempt} failed: {e}")
                time.sleep(self.delay_seconds)
        raise Exception("All retry attempts failed for trade execution.")
