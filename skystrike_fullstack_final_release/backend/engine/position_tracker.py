# backend/engine/position_tracker.py

"""
Position Tracker: computes current open positions from the trade log.
"""

import logging
import json
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)
TRADE_LOG_FILE = Path(__file__).parent.parent / "trade_log.json"

def update_open_positions() -> dict:
    """
    Reads the trade log and calculates net open positions per ticker.
    Returns a dict: {ticker: net_quantity}.
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
    except Exception as e:
        logger.error(f"Unexpected error loading trade log: {e}")
        return {}

    positions = {}
    for trade in trades:
        ticker = trade.get("ticker")
        side = trade.get("side", "").lower()
        quantity = trade.get("quantity", 0)
        # Treat sells as negative, buys as positive
        if side in ("sell_to_open", "sell_to_close"):
            net_qty = -quantity
        else:
            net_qty = quantity

        positions[ticker] = positions.get(ticker, 0) + net_qty

    # Optionally add timestamp
    result = {
        "positions": positions,
        "as_of": datetime.utcnow().isoformat()
    }
    logger.info(f"Open positions updated: {result}")
    return result

__all__ = ["update_open_positions"]
