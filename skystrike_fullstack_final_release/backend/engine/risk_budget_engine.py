# backend/engine/risk_budget_engine.py

"""
Risk Budget Engine: enforces maximum portfolio risk limits based on volatility regime.
"""

import logging
from typing import Dict, Any

from .volatility_engine import get_vix_level, classify_volatility_regime

logger = logging.getLogger(__name__)

def enforce_risk_budget(config: Dict[str, Any], max_risk: float = 0.1) -> Dict[str, Any]:
    """
    Adjusts bot contract allocations to ensure overall portfolio risk 
    does not exceed max_risk threshold. Uses volatility regime as a proxy.
    
    Args:
        config: dict mapping bot names to their config dicts, including 'contracts'.
        max_risk: float, maximum allowable risk level (0 to 1).

    Returns:
        Adjusted config dict with potentially reduced 'contracts' for riskier regimes.
    """
    vix = get_vix_level()
    regime = classify_volatility_regime(vix)
    logger.info(f"Current VIX level: {vix}, regime: {regime}, applying max_risk={max_risk}")

    adjusted_config = {}
    for bot, conf in config.items():
        original = conf.get("contracts", 0)
        # Example rule: in 'extreme' regime, cap contracts to half
        if regime == "extreme":
            adjusted = int(original * (1 - max_risk))
        elif regime == "high":
            adjusted = int(original * (1 - max_risk / 2))
        else:
            adjusted = original
        adjusted_config[bot] = {**conf, "contracts": adjusted}
    logger.info(f"Risk budget applied: {adjusted_config}")
    return adjusted_config

__all__ = ["enforce_risk_budget"]
