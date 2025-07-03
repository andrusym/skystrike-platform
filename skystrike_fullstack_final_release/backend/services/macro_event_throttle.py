
# macro_event_throttle.py

import datetime
import logging
from config import MACRO_EVENT_DATES

class MacroEventThrottle:
    def __init__(self, current_date=None):
        self.current_date = current_date or datetime.datetime.today().strftime('%Y-%m-%d')

    def should_throttle(self):
        if self.current_date in MACRO_EVENT_DATES:
            logging.info(f"[MacroThrottle] Throttle triggered for macro event: {self.current_date}")
            return True
        return False
