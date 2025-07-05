# backend/engine/bot_decay_monitor.py

"""
Monitor per-bot drawdown and signal deactivation if a threshold is exceeded.
"""

import logging
from typing import Dict

logger = logging.getLogger(__name__)

# Default drawdown threshold (e.g., 0.1 = 10%)
DEFAULT_DRAWDOWN_THRESHOLD = 0.1

# In-memory store of peak P&L per bot
_bot_peaks: Dict[str, float] = {}

def check_drawdown(bot_name: str, current_pnl: float) -> float:
    """
    Calculate the drawdown for a bot:
      drawdown = (peak_pnl - current_pnl) / peak_pnl
    Updates the stored peak if current_pnl exceeds it.
    Returns the drawdown fraction.
    """
    peak = _bot_peaks.get(bot_name, current_pnl)
    if current_pnl > peak:
        _bot_peaks[bot_name] = current_pnl
        peak = current_pnl

    if peak == 0:
        return 0.0

    drawdown = (peak - current_pnl) / peak
    logger.debug(f"Bot '{bot_name}' PnL: {current_pnl}, Peak: {peak}, Drawdown: {drawdown}")
    return drawdown

def should_deactivate_bot(
    bot_name: str,
    current_pnl: float,
    threshold: float = DEFAULT_DRAWDOWN_THRESHOLD
) -> bool:
    """
    Returns True if the bot's drawdown exceeds `threshold`.
    """
    dd = check_drawdown(bot_name, current_pnl)
    if dd > threshold:
        logger.warning(f"Bot '{bot_name}' drawdown {dd:.2%} exceeds threshold {threshold:.2%}.")
        return True
    return False

__all__ = ["check_drawdown", "should_deactivate_bot"]
