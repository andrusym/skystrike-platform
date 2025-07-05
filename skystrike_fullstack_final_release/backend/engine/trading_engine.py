# backend/engine/trading_engine.py

"""
Trading Engine: executes a built order payload via the submit_order module.
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def execute_trade(bot_name: str, order_payload: Dict[str, Any]) -> None:
    """
    Execute a single trade for the given bot.
    """
    try:
        # Lazy import to break circular dependency
        from backend.submit_order import run_bot_with_params
        logger.info(f"Executing trade for bot: {bot_name} with payload: {order_payload}")
        run_bot_with_params(bot_name, order_payload)
    except Exception as e:
        logger.error(f"Failed to execute trade for {bot_name}: {e}")
        raise

__all__ = ["execute_trade"]
