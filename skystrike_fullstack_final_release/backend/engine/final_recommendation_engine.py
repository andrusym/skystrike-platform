# backend/engine/final_recommendation_engine.py

"""Generate the final portfolio recommendation by combining ML tuning with goal-aware shifts."""

import logging

from .self_tuning_engine import run_self_tuning as self_tune
from .goal_aware_shift_engine import apply_goal_allocation

logger = logging.getLogger(__name__)

def generate_final_recommendation(user_profile: dict) -> dict:
    """
    Combines self-tuning outputs with goal-based shifts to produce
    a final portfolio configuration recommendation.
    """
    logger.info("Running self-tuning engine...")
    config = self_tune()

    logger.info("Applying goal-aware shifts...")
    final_config = shift_portfolio_by_goal(config, user_profile.get("goal", "balanced"))

    logger.info(f"Final recommendation: {final_config}")
    return final_config
