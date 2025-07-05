"""Self-Tuning Engine: computes contract allocations based on ML scores."""

import logging
from datetime import datetime
from backend.ml.ml_engine import load_ml_scores

logger = logging.getLogger(__name__)


def run_self_tuning() -> dict:
    """
    Load ML scores and compute per-bot configuration:
      - confidence > 0.75 ? 6 contracts
      - confidence > 0.5  ? 2 contracts
      - else              ? 0 contracts
    Returns a dict mapping bot names to config.
    """
    ml_scores = load_ml_scores()
    final_config = {}

    for bot, data in ml_scores.items():
        confidence = data.get("confidence", 0.0)

        if confidence > 0.75:
            contracts = 6
        elif confidence > 0.5:
            contracts = 2
        else:
            contracts = 0

        final_config[bot] = {
            "contracts": contracts,
            "active": contracts > 0,
            "confidence": round(confidence, 3),
            "timestamp": datetime.utcnow().isoformat()
        }

    logger.info(f"Self-tuning produced config: {final_config}")
    return final_config


# Aliases for downstream imports
tune_strategies_daily = run_self_tuning
get_adjusted_recommendation = run_self_tuning

__all__ = [
    "run_self_tuning",
    "tune_strategies_daily",
    "get_adjusted_recommendation",
]
