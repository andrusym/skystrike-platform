import json
import os
from datetime import datetime

RECOMMENDATION_PATH = "ml/final_recommendation.json"
CONFIG_PATH = "config/bot_config.json"
LOG_PATH = "logs/config_change_log.json"

def apply_recommendation():
    if not os.path.exists(RECOMMENDATION_PATH):
        raise FileNotFoundError("Missing final recommendation file")

    with open(RECOMMENDATION_PATH, "r") as f:
        recommendation = json.load(f)

    updated_config = {}
    for rec in recommendation:
        bot = rec["bot"]
        ticker = rec["ticker"]
        contracts = rec["contracts"]
        if bot not in updated_config:
            updated_config[bot] = {}
        updated_config[bot][ticker] = contracts

    # Write updated bot config
    with open(CONFIG_PATH, "w") as f:
        json.dump(updated_config, f, indent=2)

    # Append audit trail
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "updated_config": updated_config
    }

    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r") as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append(log_entry)

    with open(LOG_PATH, "w") as f:
        json.dump(logs, f, indent=2)

    print("[?] Bot config updated from final recommendation.")

if __name__ == "__main__":
    apply_recommendation()
