import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
# backend/schedulers/retry_if_no_trade.py

import os
import json
from datetime import datetime
from backend.bots.runner import run_bot_with_params

LOG_FILE = "logs/trade_log.json"
FALLBACK_BOT = "gridbot"
TICKER = "SPX"
CONTRACTS = 1
DTE = 0

def did_trade_today():
    if not os.path.exists(LOG_FILE):
        return False

    with open(LOG_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return False

    today = datetime.utcnow().date().isoformat()
    return any(entry.get("timestamp", "").startswith(today) for entry in data)

if __name__ == "__main__":
    if did_trade_today():
        print("✅ Trade already placed today. No retry needed.")
    else:
        print("⚠️ No trade found. Triggering fallback bot...")
        try:
            run_bot_with_params(FALLBACK_BOT, ticker=TICKER, contracts=CONTRACTS, dte=DTE)
        except Exception as e:
            print(f"❌ Error running fallback bot: {e}")
