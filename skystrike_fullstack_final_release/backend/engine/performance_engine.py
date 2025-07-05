# backend/engine/performance_engine.py

"""Compute fund-level performance metrics from trade log."""

import json
import logging
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)
TRADE_LOG_FILE = Path(__file__).parent.parent / "trade_log.json"

def compute_metrics() -> dict:
    """
    Calculate performance metrics based on executed trades:
    - total_trades: number of trades
    - wins: count of profitable trades
    - losses: count of non-profitable trades
    - win_rate: wins / total_trades
    - net_pnl: sum of all trade P&L
    - last_updated: timestamp
    """
    try:
        with open(TRADE_LOG_FILE) as f:
            trades = json.load(f)
    except FileNotFoundError:
        logger.error(f"Trade log not found: {TRADE_LOG_FILE}")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing trade log JSON: {e}")
        return {}

    total = len(trades)
    wins = sum(1 for t in trades if t.get("pnl", 0) > 0)
    losses = sum(1 for t in trades if t.get("pnl", 0) <= 0)
    net_pnl = sum(t.get("pnl", 0) for t in trades)
    win_rate = wins / total if total else 0.0

    metrics = {
        "total_trades": total,
        "wins": wins,
        "losses": losses,
        "win_rate": round(win_rate, 3),
        "net_pnl": round(net_pnl, 2),
        "last_updated": datetime.utcnow().isoformat(),
    }
    logger.debug(f"Computed performance metrics: {metrics}")
    return metrics

__all__ = ["compute_metrics"]
