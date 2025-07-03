import json
from datetime import datetime, timedelta
from pathlib import Path

MACRO_EVENTS_FILE = Path("data/macro_events.json")  # Ensure this file is kept updated

def get_macro_throttle_status():
    """
    Checks for any major macroeconomic event within the throttle window (default: 48 hours).
    If found, activates a macro throttle to suppress or reduce trading risk.
    """
    if not MACRO_EVENTS_FILE.exists():
        return {
            "macro_throttle_active": False,
            "reason": "No macro events file found",
            "timestamp": datetime.utcnow().isoformat()
        }

    try:
        with open(MACRO_EVENTS_FILE, "r") as f:
            events = json.load(f)
    except Exception as e:
        return {
            "macro_throttle_active": True,
            "reason": f"Failed to parse macro events: {str(e)}",
            "timestamp": datetime.utcnow().isoformat()
        }

    now = datetime.utcnow()
    window = timedelta(hours=48)

    for event in events:
        try:
            event_time = datetime.fromisoformat(event["timestamp"])
            if abs((event_time - now).total_seconds()) <= window.total_seconds():
                return {
                    "macro_throttle_active": True,
                    "reason": f"{event['name']} at {event['timestamp']}",
                    "timestamp": now.isoformat()
                }
        except Exception:
            continue

    return {
        "macro_throttle_active": False,
        "reason": "No imminent macro events",
        "timestamp": now.isoformat()
    }
