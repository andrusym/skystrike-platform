# backend/engine/fallback_engine.py

import os
import json
from datetime import datetime, timezone

FALLBACK_STATUS_PATH = "logs/fallback_status.json"


def get_fallback_status() -> dict:
    """
    Return current fallback engine status.
    """
    if not os.path.exists(FALLBACK_STATUS_PATH):
        return {
            "fallback_active": False,
            "reason": "No fallback_status.json file found",
            "last_updated": None
        }

    try:
        with open(FALLBACK_STATUS_PATH, "r") as f:
            data = json.load(f)
            return {
                "fallback_active": data.get("fallback_active", False),
                "reason": data.get("reason", "Unknown"),
                "last_updated": data.get("timestamp")
            }
    except Exception as e:
        return {
            "fallback_active": True,
            "reason": f"Error reading fallback status: {str(e)}",
            "last_updated": None
        }


def set_fallback_status(active: bool, reason: str = "manual override"):
    """
    Set fallback mode on/off with reason and timestamp.
    """
    status = {
        "fallback_active": active,
        "reason": reason,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    os.makedirs(os.path.dirname(FALLBACK_STATUS_PATH), exist_ok=True)
    with open(FALLBACK_STATUS_PATH, "w") as f:
        json.dump(status, f, indent=2)
