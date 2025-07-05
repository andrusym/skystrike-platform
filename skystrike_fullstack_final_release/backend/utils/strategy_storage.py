import json
import os
import time
from typing import Dict

# Resolve paths relative to project root
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DB_PATH = os.path.join(BASE_DIR, "data", "bot_metrics.json")
CONFIG_PATH = os.path.join(BASE_DIR, "data", "strategy_config.json")
COOLDOWN_LOG = os.path.join(BASE_DIR, "data", "cooldown_log.json")
RECENT_TRADES_PATH = os.path.join(BASE_DIR, "data", "recent_trades.json")


def get_strategy_metrics(bot_name: str) -> Dict:
    if not os.path.exists(DB_PATH):
        return {}
    with open(DB_PATH, "r") as f:
        data = json.load(f)
    return data.get(bot_name, {})


def update_bot_params(bot_name: str, params: dict):
    if os.path.exists(DB_PATH):
        with open(DB_PATH, "r") as f:
            data = json.load(f)
    else:
        data = {}
    data[bot_name] = {**data.get(bot_name, {}), **params}
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=2)


def get_strategy_config() -> Dict:
    if not os.path.exists(CONFIG_PATH):
        return {}
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def save_strategy_config(config: dict):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)


def log_cooldown(bot_name: str, reason: str):
    """
    Persist cooldown trigger reason and timestamp for audit.
    """
    os.makedirs(os.path.dirname(COOLDOWN_LOG), exist_ok=True)
    log = []
    if os.path.exists(COOLDOWN_LOG):
        with open(COOLDOWN_LOG, "r") as f:
            log = json.load(f)

    log.append({
        "bot": bot_name,
        "reason": reason,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    })

    with open(COOLDOWN_LOG, "w") as f:
        json.dump(log, f, indent=2)


def check_recent_trades(bot_name: str, window_minutes: int = 30) -> bool:
    """
    Returns True if a trade for the bot was recorded within the past N minutes.
    Used for cooldown checks.
    """
    now = time.time()
    if not os.path.exists(RECENT_TRADES_PATH):
        return False

    with open(RECENT_TRADES_PATH, "r") as f:
        data = json.load(f)

    last_trade_time = data.get(bot_name)
    if not last_trade_time:
        return False

    return now - last_trade_time < window_minutes * 60


def record_trade_timestamp(bot_name: str):
    """
    Stores the current timestamp for when the bot last executed a trade.
    """
    data = {}
    if os.path.exists(RECENT_TRADES_PATH):
        with open(RECENT_TRADES_PATH, "r") as f:
            data = json.load(f)

    data[bot_name] = time.time()

    with open(RECENT_TRADES_PATH, "w") as f:
        json.dump(data, f, indent=2)
