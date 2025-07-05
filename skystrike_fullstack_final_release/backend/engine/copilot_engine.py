import json

ML_SCORES_PATH = "data/ml_scores.json"
FINAL_RECOMMENDATION_PATH = "data/final_recommendation.json"

def get_top_recommendation(ticker=None, goal="balanced"):
    try:
        with open(FINAL_RECOMMENDATION_PATH, "r") as f:
            final_data = json.load(f)
    except Exception:
        with open(ML_SCORES_PATH, "r") as f:
            final_data = json.load(f)

    best = None
    for key, values in final_data.items():
        if not values.get("copilot_enabled", False):
            continue
        if ticker and not key.endswith(f":{ticker}"):
            continue
        if best is None or values["confidence"] > best["confidence"]:
            best = {
                "bot": key.split(":")[0],
                "ticker": key.split(":")[1],
                "confidence": values["confidence"],
                "contracts": values["contracts"],
                "cooldown": values.get("cooldown", False),
                "fallback_active": values.get("fallback_active", False),
                "rationale": values.get("rationale", "ML-based signal")
            }

    return best if best else {"error": "No valid recommendation found"}