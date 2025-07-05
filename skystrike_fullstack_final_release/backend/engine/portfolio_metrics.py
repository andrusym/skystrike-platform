import os
import json
from collections import defaultdict
from typing import List, Dict

TRADE_LOG_PATH = "data/trade_log.json"


def load_trade_log() -> List[dict]:
    """
    Loads the trade log from disk.
    Returns an empty list if the file doesn't exist.
    """
    if not os.path.exists(TRADE_LOG_PATH):
        return []

    with open(TRADE_LOG_PATH, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def compute_win_rate() -> float:
    """
    Calculates the win rate as: wins / (wins + losses)
    A win is defined as any trade with positive realized P&L.
    """
    trades = load_trade_log()

    wins = 0
    losses = 0

    for trade in trades:
        if trade.get("status") not in ("closed", "filled"):
            continue

        pnl = trade.get("realized_pnl", 0.0)
        if pnl > 0:
            wins += 1
        elif pnl < 0:
            losses += 1

    total = wins + losses
    if total == 0:
        return 0.0

    return round(wins / total, 4)


def compute_strategy_distribution() -> Dict[str, int]:
    """
    Counts the number of trades per strategy (e.g. ironcondor, wheel).
    """
    trades = load_trade_log()
    counts = defaultdict(int)

    for trade in trades:
        strategy = trade.get("strategy")
        if strategy:
            counts[strategy] += 1

    return dict(counts)
