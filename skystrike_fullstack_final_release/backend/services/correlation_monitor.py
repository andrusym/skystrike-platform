# correlation_monitor.py

import json
import os

def check_correlation():
    log_path = "logs/correlation_log.json"
    if not os.path.exists(log_path):
        return {"status": "no data", "correlation_matrix": {}}
    
    try:
        with open(log_path, "r") as f:
            data = json.load(f)
            return data
    except Exception as e:
        return {"status": "error", "message": str(e)}
