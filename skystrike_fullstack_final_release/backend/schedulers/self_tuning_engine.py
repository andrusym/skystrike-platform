import os
import json
from datetime import datetime
from backend.ml.ml_engine import load_ml_scores


def run_self_tuning():
    print("?? Running Self-Tuning Engine...")

    ml_scores = load_ml_scores()
    final_config = {}

    for bot, data in ml_scores.items():
        confidence = data.get("confidence", 0)

        # Contract sizing logic
        if confidence > 0.75:
            contracts = 6
        elif confidence > 0.5:
            contracts = 2
        else:
            contracts = 0

        final_config[bot] = {
            "contracts": contracts,
            "active": contracts > 0,
            "confidence": round(confidence, 3),
            "timestamp": datetime.utcnow().isoformat()
        }

    return final_config


if __name__ == "__main__":
    final_config = run_self_tuning()

    # Save to bot_config.json
    output_path = "backend/config/bot_config.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(final_config, f, indent=2)

    print("? Saved updated bot_config.json from self-tuning engine.")
