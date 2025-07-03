# backend/utils/fallback_manager.py

import json
from pathlib import Path
import datetime

def is_fallback_active():
    config_path = Path("config/fallback_config.json")
    if not config_path.exists():
        print("[??] Fallback config not found.")
        return False

    try:
        with config_path.open() as f:
            config = json.load(f)

        active_flags = {
            "ml_engine_down": config.get("ml_engine_down", False),
            "retry_mode": config.get("retry_mode", False),
            "cooldown_active": config.get("cooldown_active", False)
        }

        if any(active_flags.values()):
            print(f"[??] Fallback triggered due to: {', '.join(k for k, v in active_flags.items() if v)}")
            return True

        return False

    except Exception as e:
        print(f"[? Error reading fallback config] {e}")
        return False
