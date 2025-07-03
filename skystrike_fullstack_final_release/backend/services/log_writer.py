import os
import json
from datetime import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def append_log(log_type: str, log_entry: dict):
    path = os.path.join(LOG_DIR, f"{log_type}_log.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    log_entry["timestamp"] = datetime.now().isoformat()
    data.append(log_entry)

    with open(path, "w") as f:
        json.dump(data, f, indent=2)
