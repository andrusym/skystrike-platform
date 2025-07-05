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
STRATEGY_RUN_FILE = os.path.join(DATA_DIR, "strategy_runs.json")
FLAGGED_STRATEGIES_FILE = os.path.join(DATA_DIR, "flagged_strategies.json")

def save_journal_entry(entry: Dict[str, Any]) -> None:
    entries = []
    if os.path.exists(JOURNAL_PATH):
        try:
            with open(JOURNAL_PATH, "r") as f:
                entries = json.load(f)
        except json.JSONDecodeError:
            pass
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
    return [e for e in entries if e.get("user_id") == user_id] if user_id else entries

def log_trade(trade: Dict[str, Any]) -> None:
    trades = []
    if os.path.exists(TRADE_LOG_PATH):
        try:
            with open(TRADE_LOG_PATH, "r") as f:
                trades = json.load(f)
        except json.JSONDecodeError:
            pass
    trade.setdefault("timestamp", datetime.utcnow().isoformat())
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
    return [t for t in trades if t.get("bot") == bot_name] if bot_name else trades

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
    entry = {
        "bot": bot_name,
        "timestamp": datetime.utcnow().isoformat(),
        "reason": reason
    }
    entries = []
    if os.path.exists(COOLDOWN_LOG_PATH):
        try:
            with open(COOLDOWN_LOG_PATH, "r") as f:
                entries = json.load(f)
        except json.JSONDecodeError:
            pass
    entries.append(entry)
    with open(COOLDOWN_LOG_PATH, "w") as f:
        json.dump(entries, f, indent=2)

def check_recent_trades(bot_name: str, within_minutes: int = 60) -> bool:
    cutoff = datetime.utcnow() - timedelta(minutes=within_minutes)
    for t in reversed(load_trade_log(bot_name)):
        try:
            if datetime.fromisoformat(t.get("timestamp")) >= cutoff:
                return True
        except Exception:
            continue
    return False

def get_strategy_run_data(strategy_id: str) -> dict:
    if not os.path.exists(STRATEGY_RUN_FILE):
        return {}
    with open(STRATEGY_RUN_FILE, "r") as f:
        data = json.load(f)
    return data.get(strategy_id, {})

def flag_strategy(strategy_id: str, reason: str = "burnout") -> None:
    flags = {}
    if os.path.exists(FLAGGED_STRATEGIES_FILE):
        with open(FLAGGED_STRATEGIES_FILE, "r") as f:
            flags = json.load(f)
    flags[strategy_id] = {"reason": reason}
    with open(FLAGGED_STRATEGIES_FILE, "w") as f:
        json.dump(flags, f, indent=2)

def get_paused_strategies() -> list:
    config = get_strategy_config()
    return [s for s, props in config.items() if props.get("status") == "paused"]

def score_strategy(strategy: str) -> float:
    return 0.8  # placeholder ML score

def reprice_trade(strategy: str) -> dict:
    return {
        "strategy": strategy,
        "ticker": "SPY",
        "qty": 1,
        "price": 1.0,
        "account_id": "demo"
    }

def reenter_trade(trade: dict) -> dict:
    log_trade(trade)
    return {"status": "submitted", "trade": trade}

def get_bot_performance(bot: str) -> dict:
    # Placeholder logic – replace with real performance metrics
    return {
        "win_rate": 0.75,
        "drawdown": -0.05,
        "active": True
    }

def deactivate_bot(bot: str) -> None:
    config = get_strategy_config()
    if bot in config:
        config[bot]["status"] = "paused"
        save_strategy_config(config)

def reactivate_bot(bot: str) -> None:
    config = get_strategy_config()
    if bot in config:
        config[bot]["status"] = "active"
        save_strategy_config(config)
