import json
import os
from backend.engine.self_tuning_engine import run_self_tuning as self_tune
from backend.engine.goal_aware_shift_engine import run_goal_aware_shift as shift_for_goal

# ? Output paths (inside backend/ml/)
SELF_TUNE_OUTPUT = "ml/self_tune_output.json"
FINAL_OUTPUT = "ml/final_recommendation.json"
PORTFOLIO_PATH = "ml/portfolio_profiles.json"

def run_final_recommendation():
    # Step 1: Run self-tuning engine and save scores
    self_tuned = self_tune()
    with open(SELF_TUNE_OUTPUT, "w") as f:
        json.dump(self_tuned, f, indent=2)

    # Step 2: Determine user goal
    if not os.path.exists(PORTFOLIO_PATH):
        user_goal = "balanced"
    else:
        with open(PORTFOLIO_PATH, "r") as f:
            profile_data = json.load(f)
            user_goal = profile_data.get("goal", "balanced").lower()

    # Step 3: Apply goal-aware contract sizing
    adjusted = shift_for_goal(user_goal)

    # Step 4: Combine into final recommendation
    final_result = {
        "goal": user_goal,
        "bot_status": self_tuned,
        "adjusted_allocation": adjusted
    }

    with open(FINAL_OUTPUT, "w") as f:
        json.dump(final_result, f, indent=2)

    print(f"? Final recommendation written to {FINAL_OUTPUT}")
    return final_result

# CLI entrypoint
if __name__ == "__main__":
    result = run_final_recommendation()
    print(json.dumps(result, indent=2))

generate_final_recommendation = run_final_recommendation
