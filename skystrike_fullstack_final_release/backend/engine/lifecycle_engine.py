import json
from datetime import datetime, timedelta

CONFIG_PATH = "data/bot_config.json"

def load_bot_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def save_bot_config(data):
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=2)

def check_degrade_status(bot_name, metrics):
    loss_streak = metrics.get("loss_streak", 0)
    win_rate = metrics.get("win_rate", 1.0)
    if loss_streak >= 3 or win_rate < 0.4:
        return True
    return False

def apply_cooldown(bot_name):
    config = load_bot_config()
    if bot_name in config:
        config[bot_name]["status"] = "cooldown"
        config[bot_name]["cooldown_until"] = (datetime.utcnow() + timedelta(days=1)).isoformat()
        save_bot_config(config)

def is_in_cooldown(bot_name):
    config = load_bot_config()
    bot = config.get(bot_name, {})
    if bot.get("status") == "cooldown":
        until = datetime.fromisoformat(bot.get("cooldown_until", "1970-01-01T00:00:00"))
        if datetime.utcnow() < until:
            return True
    return False
