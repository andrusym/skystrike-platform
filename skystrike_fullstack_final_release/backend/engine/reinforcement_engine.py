# backend/engine/reinforcement_engine.py

"""
Reinforcement Engine: adjusts allocation based on reinforcement learning signals.
"""

import logging

logger = logging.getLogger(__name__)

def adapt_allocation(config: dict, market_feedback: dict = None) -> dict:
    """
    Modify allocation config based on reinforcement learning feedback.
    `config`: dict of bot configurations {bot_name: {"contracts": int, ...}}
    `market_feedback`: optional dict containing recent performance metrics.
    Returns updated config.
    """
    updated = {}
    for bot, conf in config.items():
        contracts = conf.get("contracts", 0)
        confidence = conf.get("confidence", 0.0)
        # Basic rule: if confidence < 0.3, reduce contracts by half
        if confidence < 0.3:
            new_contracts = max(0, int(contracts * 0.5))
        else:
            new_contracts = contracts
        updated[bot] = {**conf, "contracts": new_contracts}
    logger.info(f"Adapted allocation: {updated}")
    return updated

__all__ = ["adapt_allocation"]
