import json
from datetime import datetime, timedelta, date
import os

def get_expirations(count=2):
    today = datetime.now().date()
    expirations = []
    while len(expirations) < count:
        if today.weekday() < 5:
            expirations.append(today)
        today += timedelta(days=1)
    return expirations

def format_tradier_option_symbol(ticker: str, exp: date, call_put: str, strike: float) -> str:
    root = ticker.upper().ljust(6)
    exp_str = exp.strftime('%y%m%d')
    cp = 'C' if call_put.upper() == 'C' else 'P'
    strike_formatted = f"{int(strike * 1000):08d}"
    return f"{root}{exp_str}{cp}{strike_formatted}"

def load_json(path: str):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

def save_json(path: str, data: dict):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def append_log(path: str, record: dict):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    log = []
    if os.path.exists(path):
        with open(path, "r") as f:
            try:
                log = json.load(f)
            except:
                log = []
    log.append(record)
    with open(path, "w") as f:
        json.dump(log, f, indent=2)
