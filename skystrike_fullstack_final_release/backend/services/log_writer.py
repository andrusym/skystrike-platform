import os
import json
from datetime import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def append_log(name: str, payload: dict):
    path = os.path.join(LOG_DIR, f"{name}.json")
    try:
        if os.path.exists(path):
            with open(path, "r") as f:
                data = json.load(f)
        else:
            data = []
        payload["timestamp"] = datetime.utcnow().isoformat()
        data.append(payload)
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"[log_writer] Failed to write to {path}: {e}")
