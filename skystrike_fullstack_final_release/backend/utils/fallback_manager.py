import json
import os

FALLBACK_CONFIG_PATH = "config/fallback_config.json"

def load_fallback_config():
    if not os.path.exists(FALLBACK_CONFIG_PATH):
        return {
            "ml_engine_down": False,
            "retry_mode": False,
            "cooldown_active": False,
            "last_trigger": None,
            "notes": "Default fallback config"
        }
    with open(FALLBACK_CONFIG_PATH, "r") as f:
        return json.load(f)

def is_fallback_active() -> bool:
    config = load_fallback_config()
    return config.get("ml_engine_down") or config.get("retry_mode") or config.get("cooldown_active")
