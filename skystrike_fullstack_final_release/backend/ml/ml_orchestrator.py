#!/usr/bin/env python3
# coding: utf-8

from backend.ml.generate_ml_scores import generate_ml_scores
from backend.engine.goal_aware_shift_engine import apply_goal_allocation
from backend.engine.final_recommendation_engine import generate_final_recommendation
from backend.shared.utils import save_json, append_log
from datetime import datetime

def run_ml_pipeline(goal: str = "balanced"):
    print("Generating ML scores...")
    generate_ml_scores()

    print("Running goal-aware shift...")
    run_goal_aware_shift(goal)

    print("Running final recommendation...")
    final = run_final_recommendation()

    # Save to bot_config.json
    save_json("bot_config.json", final)

    # Log change
    append_log("logs/config_change_log.json", {
        "timestamp": datetime.utcnow().isoformat(),
        "source":    "ml_pipeline",
        "goal":      goal,
        "recommendation": final
    })

    print("ML pipeline complete.")
    return final
