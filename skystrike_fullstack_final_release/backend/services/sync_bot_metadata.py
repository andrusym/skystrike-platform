import json
import os
from datetime import datetime

BOT_CONFIG_PATH = "config/bot_config.json"
TRADE_LOG_PATH = "data/trade_log.json"

DEFAULT_FIELDS = {
    "status": "disabled",
    "ticker": "SPY",
    "confidence": 0.5,
    "type": "other",
    "last_run": "N/A",
    "pnl": 0.0
}

# Optional: categorize bots by known names
BOT_TYPE_MAPPING = {
    "ironcondor": "condor",
    "kingcondor": "condor",
    "trendbot": "trend",
    "momentumbot": "trend",
    "wheel": "wheel",
    "csp": "wheel",
    "spread": "spread",
    "replicator": "replicator",
    "pairstrader": "pair",
    "dcabot": "dca",
    "scalper": "scalp",
    "copybot": "copy",
    "gridbot": "grid",
    "squeezebot": "squeeze"
}

def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def get_latest_pnl_for_bot(bot_name, trade_log):
    trades = [t for t in trade_log if t.get("strategy", "").lower() == bot_name.lower()]
    if not trades:
        return 0.0, "N/A"
    sorted_trades = sorted(trades, key=lambda t: t.get("timestamp", ""), reverse=True)
    latest = sorted_trades[0]
    pnl = latest.get("pnl", 0.0)
    ts = latest.get("timestamp", "N/A")
    return pnl, ts

def sync_bot_metadata():
    config = load_json(BOT_CONFIG_PATH)
    trade_log = load_json(TRADE_LOG_PATH)

    for bot_name, meta in config.items():
        for key, default in DEFAULT_FIELDS.items():
            meta.setdefault(key, default)

        # Inject type if missing
        if meta["type"] == "other":
            for key, val in BOT_TYPE_MAPPING.items():
                if key in bot_name.lower():
                    meta["type"] = val
                    break

        # Update P&L and last_run
        pnl, ts = get_latest_pnl_for_bot(bot_name, trade_log)
        meta["pnl"] = pnl
        meta["last_run"] = ts

    save_json(BOT_CONFIG_PATH, config)
    return {"message": "Bot metadata synced", "bots": config}

if __name__ == "__main__":
    print(sync_bot_metadata())