# backend/engine/goal_aware_shift_engine.py

"""
Adjust portfolio allocation based on user-defined goal profiles.

Supported goals:
- 'growth': Boost position sizes by 10%
- 'income': Reduce position sizes by 10%
- 'balanced': Leave config unchanged

This logic is applied on top of ML-driven recommendations.
"""

import logging
from copy import deepcopy

logger = logging.getLogger(__name__)

def apply_goal_allocation(config: dict, goal: str) -> dict:
    """
    Apply user goal-based allocation adjustments to the config.

    Args:
        config (dict): ML-generated contract config per bot.
        goal (str): One of ['growth', 'income', 'balanced'].

    Returns:
        dict: Adjusted configuration.
    """
    adjusted_config = deepcopy(config)
    for bot, conf in adjusted_config.items():
        base_contracts = conf.get("contracts", 0)
        if goal == "growth":
            conf["contracts"] = max(1, int(base_contracts * 1.1))
        elif goal == "income":
            conf["contracts"] = max(1, int(base_contracts * 0.9))
        # For 'balanced' or unknown goal, keep original
        conf["adjusted_for_goal"] = goal
    logger.info(f"Applied goal allocation '{goal}': {adjusted_config}")
    return adjusted_config

__all__ = ["apply_goal_allocation"]
