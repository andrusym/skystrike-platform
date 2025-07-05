# backend/utils/logger.py

import os
from datetime import datetime

LOG_PATH = os.path.join(os.path.dirname(__file__), "../../data/event_log.json")

def append_log(event: str, payload: dict):
    timestamp = datetime.utcnow().isoformat()
    log_entry = {"timestamp": timestamp, "event": event, "payload": payload}

    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

    try:
        if os.path.exists(LOG_PATH):
            with open(LOG_PATH, "a") as f:
                f.write(",\n" + str(log_entry))
        else:
            with open(LOG_PATH, "w") as f:
                f.write("[\n" + str(log_entry))
    except Exception as e:
        print(f"[ERROR] Failed to write log: {e}")

