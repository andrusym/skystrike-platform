import json
import os
from datetime import datetime

METRICS_PATH = "data/bot_metrics.json"
OUTPUT_PATH = "backend/ml/ml_scores.json"

def compute_confidence(win_rate: float, pnl: float) -> float:
    base = 0.5
    if win_rate is not None:
        base += (win_rate - 0.5) * 0.8
    if pnl is not None:
        base += min(pnl / 1000.0, 0.2)
    return round(min(max(base, 0.1), 0.99), 3)

def generate_ml_scores():
    if not os.path.exists(METRICS_PATH):
        print(f"⚠️ Missing {METRICS_PATH}")
        return

    with open(METRICS_PATH, "r") as f:
        metrics = json.load(f)

    now = datetime.utcnow().isoformat()
    scores = {}

    for bot, data in metrics.items():
        win_rate = data.get("win_rate")
        pnl = data.get("total_pnl", 0)
        confidence = compute_confidence(win_rate, pnl)
        scores[bot] = {
            "confidence": confidence,
            "timestamp": now
        }

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(scores, f, indent=2)
    print("✅ ML scores updated.")

if __name__ == "__main__":
    generate_ml_scores()
