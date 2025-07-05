import json
import os
from datetime import datetime, timedelta

# File paths
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "../../data"))

DB_PATH = os.path.join(DATA_DIR, "bot_metrics.json")
CONFIG_PATH = os.path.join(DATA_DIR, "strategy_config.json")
TRADE_LOG_PATH = os.path.join(DATA_DIR, "trade_log.json")
COOLDOWN_LOG_PATH = os.path.join(DATA_DIR, "cooldown_log.json")


def get_strategy_metrics(bot_name: str) -> dict:
    if not os.path.exists(DB_PATH):
        return {}
    try:
        with open(DB_PATH, 'r') as f:
            data = json.load(f)
        return data.get(bot_name, {})
    except json.JSONDecodeError:
        return {}


def update_bot_params(bot_name: str, params: dict) -> None:
    data = {}
    if os.path.exists(DB_PATH):
        try:
            with open(DB_PATH, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = {}

    data[bot_name] = {**data.get(bot_name, {}), **params}

    with open(DB_PATH, 'w') as f:
        json.dump(data, f, indent=2)


def get_strategy_config() -> dict:
    if not os.path.exists(CONFIG_PATH):
        return {}
    try:
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}


def save_strategy_config(config: dict) -> None:
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2)


def log_cooldown(bot_name: str, reason: str) -> None:
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "bot": bot_name,
        "reason": reason
    }

    cooldowns = []
    if os.path.exists(COOLDOWN_LOG_PATH):
        try:
            with open(COOLDOWN_LOG_PATH, 'r') as f:
                cooldowns = json.load(f)
        except json.JSONDecodeError:
            cooldowns = []

    cooldowns.append(entry)

    with open(COOLDOWN_LOG_PATH, 'w') as f:
        json.dump(cooldowns, f, indent=2)

    print(f"[Cooldown] {bot_name} triggered: {reason}")


def check_recent_trades(bot_name: str, minutes: int = 15) -> bool:
    if not os.path.exists(TRADE_LOG_PATH):
        return False

    cutoff = datetime.utcnow() - timedelta(minutes=minutes)

    try:
        with open(TRADE_LOG_PATH, 'r') as f:
            trades = json.load(f)
    except json.JSONDecodeError:
        return False

    for trade in trades:
        ts = trade.get("timestamp")
        name = trade.get("bot")
        if not ts or name != bot_name:
            continue
        try:
            t = datetime.fromisoformat(ts)
            if t > cutoff:
                return True
        except ValueError:
            continue

    return False
