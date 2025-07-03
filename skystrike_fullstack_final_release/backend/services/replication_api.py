
import json
import os
from datetime import datetime
from dotenv import load_dotenv
from backend.utils.trade_logger import log_trade

load_dotenv()

TRADE_LOG_PATH = os.getenv("TRADE_LOG_PATH", "trade_log.json")

def load_trade_log():
    try:
        with open(TRADE_LOG_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def replicate_trade(trade):
    # Modify or replay a trade entry as needed
    trade_copy = trade.copy()
    trade_copy["timestamp"] = datetime.utcnow().isoformat()
    trade_copy["replicated"] = True
    log_trade(trade_copy)
    return trade_copy

def run_replication(limit=5):
    trade_log = load_trade_log()
    if not trade_log:
        return {"status": "no trades to replicate"}

    recent_trades = sorted(trade_log, key=lambda x: x.get("timestamp", ""), reverse=True)[:limit]
    replicated = []

    for trade in recent_trades:
        new_trade = replicate_trade(trade)
        replicated.append(new_trade)

    return {
        "status": "replication complete",
        "replicated_count": len(replicated),
        "replicated_trades": replicated
    }
