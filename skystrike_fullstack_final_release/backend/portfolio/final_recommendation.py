# backend/portfolio/final_recommendation.py

import os
import json
from datetime import datetime

from backend.engine.goal_aware_shift_engine import apply_goal_allocation
from backend.engine.self_tuning_engine import get_adjusted_recommendation  # ? Updated import

FINAL_RECOMMENDATION_LOG = "logs/final_recommendation.json"


def get_final_recommendation() -> dict:
    """
    Returns the latest final recommendation from file, or generates one if missing.
    """
    if os.path.exists(FINAL_RECOMMENDATION_LOG):
        try:
            with open(FINAL_RECOMMENDATION_LOG, "r") as f:
                return json.load(f)
        except Exception as e:
            return {"error": f"Failed to read final recommendation: {str(e)}"}

    # Fallback to generating a new one
    return run_final_recommendation()


def run_final_recommendation(goal: str = "balanced") -> dict:
    """
    Generates the ML + goal-aware final sizing recommendation for all bots.
    """
    base = get_adjusted_recommendation()  # ? Renamed to match engine
    shifted = apply_goal_allocation(base, goal)

    final = {
        "timestamp": datetime.utcnow().isoformat(),
        "goal": goal,
        "base": base,
        "final": shifted
    }

    os.makedirs(os.path.dirname(FINAL_RECOMMENDATION_LOG), exist_ok=True)
    with open(FINAL_RECOMMENDATION_LOG, "w") as f:
        json.dump(final, f, indent=2)

    return final
