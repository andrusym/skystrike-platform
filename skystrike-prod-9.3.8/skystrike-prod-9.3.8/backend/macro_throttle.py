# macro_throttle.py
from datetime import datetime

event_days = ["2025-07-15", "2025-08-02"]  # CPI, FOMC examples

def is_macro_event_day():
    today = datetime.now().strftime("%Y-%m-%d")
    return today in event_days
