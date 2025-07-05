import os
import json
from datetime import datetime
from backend.ml.ml_engine import load_ml_scores

def evaluate_market_conditions():
    ml_scores = load_ml_scores()
    for bot, score in ml_scores.items():
        score["confidence"] = round(max(0, min(1, score["confidence"] + 0.01)), 3)
        score["timestamp"] = datetime.utcnow().isoformat()

    os.makedirs("backend/ml", exist_ok=True)
    with open("backend/ml/ml_scores.json", "w") as f:
        json.dump(ml_scores, f, indent=2)
    print("✅ Confidence scores updated.")

if __name__ == "__main__":
    evaluate_market_conditions()
