import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TRADE_LOG_PATH = os.path.join(BASE_DIR, 'logs', 'trade_log.json')

def load_trade_log():
    """Load and return the trade log entries."""
    if not os.path.exists(TRADE_LOG_PATH):
        return []
    with open(TRADE_LOG_PATH, 'r') as f:
        return json.load(f)
