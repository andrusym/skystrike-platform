import json
from datetime import datetime

TRADE_LOG_PATH = "data/trade_log.json"

def evaluate_exit_conditions(threshold_profit=0.5, threshold_loss=-1.0):
    try:
        with open(TRADE_LOG_PATH, "r") as f:
            trades = json.load(f)
    except Exception:
        print("Trade log not found or invalid.")
        return []

    exit_signals = []

    for trade in trades:
        if trade.get("status") != "open":
            continue

        pnl = trade.get("pnl", 0.0)
        bot = trade.get("bot")
        symbol = trade.get("symbol")

        if pnl >= threshold_profit:
            reason = "Target profit hit"
        elif pnl <= threshold_loss:
            reason = "Stop-loss triggered"
        else:
            continue

        exit_signals.append({
            "bot": bot,
            "symbol": symbol,
            "pnl": pnl,
            "reason": reason,
            "timestamp": datetime.utcnow().isoformat()
        })

    return exit_signals