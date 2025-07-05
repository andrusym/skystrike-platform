# backend/utils/trade_logger.py

import json
from pathlib import Path
from threading import Lock
from typing import Any, Dict, List, Union

# Path to your trade log file
LOG_PATH = Path(__file__).parent.parent / "data" / "trade_log.json"

# A lock to ensure thread-safe writes
_write_lock = Lock()


def load_trade_log() -> Union[Dict[str, Any], List[Any]]:
    """
    Load and return the entire trade log from disk.
    Returns either a dict or a list, depending on the JSON structure.
    """
    if not LOG_PATH.exists():
        return []
    with LOG_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def get_trade_log() -> Union[Dict[str, Any], List[Any]]:
    """
    Alias for load_trade_log(), so routes can import get_trade_log().
    """
    return load_trade_log()


def save_trade_log(log: Union[Dict[str, Any], List[Any]]) -> None:
    """
    Overwrite the trade log on disk with the given data.
    """
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with _write_lock, LOG_PATH.open("w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)


def append_trade(entry: Dict[str, Any]) -> None:
    """
    Append a single trade entry to the log.
    If the log is a list, append to it; if it's a dict, merge keys.
    """
    log = load_trade_log()
    if isinstance(log, list):
        log.append(entry)
    elif isinstance(log, dict):
        log.update(entry)
    else:
        log = [log, entry]

    save_trade_log(log)
