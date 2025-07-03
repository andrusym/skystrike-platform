import json
import os

# Existing path for bot metrics
DB_PATH = os.path.join(os.path.dirname(__file__), '../../data/bot_metrics.json')
CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../../data/strategy_config.json')


def get_strategy_metrics(bot_name: str):
    if not os.path.exists(DB_PATH):
        return {}
    with open(DB_PATH, 'r') as f:
        data = json.load(f)
    return data.get(bot_name, {})


def update_bot_params(bot_name: str, params: dict):
    if os.path.exists(DB_PATH):
        with open(DB_PATH, 'r') as f:
            data = json.load(f)
    else:
        data = {}
    data[bot_name] = {**data.get(bot_name, {}), **params}
    with open(DB_PATH, 'w') as f:
        json.dump(data, f, indent=2)


def get_strategy_config():
    if not os.path.exists(CONFIG_PATH):
        return {}
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)


def save_strategy_config(config: dict):
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2)

def log_cooldown(bot_name: str, reason: str):
    # Placeholder: log the cooldown trigger for the bot
    print(f"[Cooldown] {bot_name} triggered: {reason}")

def check_recent_trades(bot_name: str) -> bool:
    # Placeholder: return True if recent trades exist (simulate cooldown logic)
    return False
