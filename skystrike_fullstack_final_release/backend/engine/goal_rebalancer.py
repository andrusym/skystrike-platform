import json

ML_SCORES_PATH = "data/ml_scores.json"

def run_goal_aware_shift(goal: str = "balanced") -> dict:
    with open(ML_SCORES_PATH, "r") as f:
        ml_scores = json.load(f)

    result = {}
    for key, info in ml_scores.items():
        confidence = info.get("confidence", 0)
        base_contracts = info.get("contracts", 0)

        # Goal-based adjustment
        if goal == "growth":
            contracts = base_contracts
        elif goal == "balanced":
            contracts = max(1, round(base_contracts * 0.66)) if base_contracts >= 2 else base_contracts
        elif goal == "preservation":
            contracts = 1 if base_contracts >= 2 else 0
        else:
            contracts = base_contracts

        result[key] = {
            "confidence": confidence,
            "contracts": contracts,
            "cooldown": info.get("cooldown", False),
            "fallback_active": info.get("fallback_active", False),
            "rationale": info.get("rationale", ""),
            "copilot_enabled": contracts > 0
        }

    return result