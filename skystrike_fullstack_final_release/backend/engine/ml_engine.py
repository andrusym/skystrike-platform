def score_strategy(strategy_name, ticker, setup):
    return 0.85
import json

def load_ml_scores():
    with open("data/ml_scores.json", "r") as f:
        return json.load(f)

def evaluate_ml_status(scores: dict) -> str:
    if not scores:
        return "inactive"
    avg = sum(scores.get(bot, {}).get("confidence", 0) for bot in scores) / len(scores)
    return "active" if avg >= 0.5 else "degraded"
