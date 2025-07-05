import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Base data directory
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "../../data"))

# File paths
JOURNAL_PATH = os.path.join(DATA_DIR, "journal_entries.json")
TRADE_LOG_PATH = os.path.join(DATA_DIR, "trade_log.json")
CONFIG_PATH = os.path.join(DATA_DIR, "strategy_config.json")
COOLDOWN_LOG_PATH = os.path.join(DATA_DIR, "cooldown_log.json")


def save_journal_entry(entry: Dict[str, Any]) -> None:
    if not os.path.exists(JOURNAL_PATH):
        entries = []
    else:
        try:
            with open(JOURNAL_PATH, "r") as f:
                entries = json.load(f)
        except json.JSONDecodeError:
            entries = []

    entries.append(entry)

    with open(JOURNAL_PATH, "w") as f:
        json.dump(entries, f, indent=2)


def load_journal_entries(user_id: str = None) -> List[Dict[str, Any]]:
    if not os.path.exists(JOURNAL_PATH):
        return []

    try:
        with open(JOURNAL_PATH, "r") as f:
            entries = json.load(f)
    except json.JSONDecodeError:
        return []

    if user_id:
        entries = [e for e in entries if e.get("user_id") == user_id]

    return entries


def log_trade(trade: Dict[str, Any]) -> None:
    if not os.path.exists(TRADE_LOG_PATH):
        trades = []
    else:
        try:
            with open(TRADE_LOG_PATH, "r") as f:
                trades = json.load(f)
        except json.JSONDecodeError:
            trades = []

    if "timestamp" not in trade:
        trade["timestamp"] = datetime.utcnow().isoformat()

    trades.append(trade)

    with open(TRADE_LOG_PATH, "w") as f:
        json.dump(trades, f, indent=2)


def load_trade_log(bot_name: str = None) -> List[Dict[str, Any]]:
    if not os.path.exists(TRADE_LOG_PATH):
        return []

    try:
        with open(TRADE_LOG_PATH, "r") as f:
            trades = json.load(f)
    except json.JSONDecodeError:
        return []

    if bot_name:
        trades = [t for t in trades if t.get("bot") == bot_name]

    return trades


def get_strategy_config() -> Dict[str, Any]:
    if not os.path.exists(CONFIG_PATH):
        return {}
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}


def save_strategy_config(config: Dict[str, Any]) -> None:
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)


def log_cooldown(bot_name: str, reason: str = "") -> None:
    """
    Log a cooldown event for a bot
    """
    cooldown_entry = {
        "bot": bot_name,
        "timestamp": datetime.utcnow().isoformat(),
        "reason": reason
    }

    if not os.path.exists(COOLDOWN_LOG_PATH):
        entries = []
    else:
        try:
            with open(COOLDOWN_LOG_PATH, "r") as f:
                entries = json.load(f)
        except json.JSONDecodeError:
            entries = []

    entries.append(cooldown_entry)

    with open(COOLDOWN_LOG_PATH, "w") as f:
        json.dump(entries, f, indent=2)


def check_recent_trades(bot_name: str, within_minutes: int = 60) -> bool:
    """
    Check if a bot has traded in the last `within_minutes`
    """
    now = datetime.utcnow()
    cutoff = now - timedelta(minutes=within_minutes)

    trades = load_trade_log(bot_name)

    for t in reversed(trades):
        try:
            trade_time = datetime.fromisoformat(t.get("timestamp"))
            if trade_time >= cutoff:
                return True
        except Exception:
            continue

    return False
