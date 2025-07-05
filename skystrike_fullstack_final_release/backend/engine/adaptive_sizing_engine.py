# backend/engine/adaptive_sizing_engine.py

"""
Adaptive Sizing Engine: scales contract counts based on provided multiplier or ML confidence.
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def adjust_contract_size(
    config: Dict[str, Any],
    multiplier: float = 1.0
) -> Dict[str, Any]:
    """
    Multiply each bot’s contract count by `multiplier`.
    E.g., to bump size by 10%, use multiplier=1.1.
    """
    adjusted = {}
    for bot, conf in config.items():
        base = conf.get("contracts", 0)
        new_ct = int(base * multiplier)
        adjusted[bot] = {**conf, "contracts": new_ct}
    logger.info(f"Adjusted contract sizes with multiplier {multiplier}: {adjusted}")
    return adjusted

__all__ = ["adjust_contract_size"]
