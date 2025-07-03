
from backend.engine.generate_ml_scores import generate_ml_scores
from backend.engine.goal_aware_shift_engine import run_goal_aware_shift
from backend.engine.final_recommendation_engine import run_final_recommendation
from backend.shared.utils import save_json, append_log
from datetime import datetime
import os

def run_ml_pipeline(goal="balanced"):
    print("🧠 Generating ML scores...")
    generate_ml_scores()

    print("🎯 Running goal-aware shift...")
    run_goal_aware_shift(goal)

    print("✅ Running final recommendation...")
    final = run_final_recommendation()

    # Save to bot_config.json
    save_json("bot_config.json", final)

    # Log change
    append_log("logs/config_change_log.json", {
        "timestamp": datetime.now().isoformat(),
        "source": "ml_pipeline",
        "goal": goal,
        "recommendation": final
    })

    print("🚀 ML pipeline complete.")
    return final
