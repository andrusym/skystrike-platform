import json
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("data/trade_log.json")

def log_trade(strategy: str, ticker: str, contracts: int, legs: list, response: dict, meta: dict = None):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "strategy": strategy,
        "ticker": ticker,
        "contracts": contracts,
        "legs": legs,
        "broker_response": response,
        "meta": meta or {},
        "status": "OPEN"
    }

    if LOG_FILE.exists():
        with open(LOG_FILE, "r+") as f:
            data = json.load(f)
            data.append(entry)
            f.seek(0)
            json.dump(data, f, indent=2)
    else:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, "w") as f:
            json.dump([entry], f, indent=2)

def load_trade_log():
    if not LOG_FILE.exists():
        return []
    with open(LOG_FILE, "r") as f:
        return json.load(f)
