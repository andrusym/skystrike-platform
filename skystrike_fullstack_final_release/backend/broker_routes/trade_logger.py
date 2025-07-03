
import json
import os
import datetime

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "trades_log.jsonl")

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

def log_trade(trade, closed=False):
    log_entry = {
        "id": trade["id"],
        "ticker": trade["ticker"],
        "strategy": trade["strategy"],
        "entry_time": trade["entry_time"],
        "status": trade["status"],
        "legs": trade.get("legs", {}),
        "mode": trade.get("mode", "paper"),
        "capital": trade.get("capital", 0),
        "entry_price": trade.get("entry_price", 0),
        "target_exit": trade.get("target_exit", 0),
        "timestamp": datetime.datetime.now().isoformat()
    }

    if closed:
        log_entry.update({
            "exit_time": trade.get("exit_time"),
            "exit_price": trade.get("exit_price"),
            "pnl": trade.get("pnl"),
            "reason": trade.get("reason", "manual")
        })

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    print(f"Trade logged: {log_entry['id']} ({'CLOSED' if closed else 'OPEN'})")

def get_trade_log():
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r") as f:
        return [json.loads(line.strip()) for line in f if line.strip()]
