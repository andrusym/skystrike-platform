import json
from datetime import datetime
import os

TRADE_LOG = "data/trade_log.json"
DRAWDOWN_FILE = "data/bot_drawdowns.json"
COOLDOWN_THRESHOLD = -0.10  # 10% drawdown
STARTING_CAPITAL = 10000

def compute_drawdowns():
    try:
        with open(TRADE_LOG, "r") as f:
            trades = json.load(f)
    except:
        return {"error": "Trade log unreadable"}

    equity_curves = {}
    drawdown_status = {}

    for trade in trades:
        key = trade.get("bot")
        if key not in equity_curves:
            equity_curves[key] = [STARTING_CAPITAL]
        prev = equity_curves[key][-1]
        pnl = trade.get("pnl", 0)
        new_val = prev + pnl
        equity_curves[key].append(new_val)

    for bot, curve in equity_curves.items():
        peak = max(curve)
        trough = min(curve)
        drawdown_pct = (trough - peak) / peak if peak else 0
        cooldown = drawdown_pct <= COOLDOWN_THRESHOLD
        drawdown_status[bot] = {
            "max_drawdown": round(drawdown_pct, 4),
            "cooldown_triggered": cooldown,
            "last_equity": round(curve[-1], 2),
            "last_updated": datetime.utcnow().isoformat()
        }

    with open(DRAWDOWN_FILE, "w") as f:
        json.dump(drawdown_status, f, indent=2)

    return drawdown_status