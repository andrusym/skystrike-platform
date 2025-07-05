import json
import os
from datetime import datetime

TRADE_LOG = "data/trade_log.json"
GUARDRAIL_FILE = "data/guardrail_status.json"
STARTING_EQUITY = 100000
DRAWDOWN_LIMIT = 0.15  # 15%

def check_equity_guardrail():
    try:
        with open(TRADE_LOG, "r") as f:
            trades = json.load(f)
    except:
        return {"error": "Trade log unreadable"}

    equity = STARTING_EQUITY
    for trade in trades:
        equity += trade.get("pnl", 0)

    drawdown = (STARTING_EQUITY - equity) / STARTING_EQUITY
    triggered = drawdown >= DRAWDOWN_LIMIT

    status = {
        "drawdown_pct": round(drawdown, 4),
        "guardrail_triggered": triggered,
        "current_equity": round(equity, 2),
        "timestamp": datetime.utcnow().isoformat()
    }

    with open(GUARDRAIL_FILE, "w") as f:
        json.dump(status, f, indent=2)

    return status