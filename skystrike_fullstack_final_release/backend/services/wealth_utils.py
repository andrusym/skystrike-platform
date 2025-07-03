import json
from datetime import datetime

CONFIG_PATH = "data/wealth_config.json"
LOG_PATH = "data/wealth_log.json"

def load_wealth_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def save_wealth_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)

def log_wealth_event(event):
    try:
        with open(LOG_PATH, "r+") as f:
            log = json.load(f)
            log.append(event)
            f.seek(0)
            json.dump(log, f, indent=2)
    except FileNotFoundError:
        with open(LOG_PATH, "w") as f:
            json.dump([event], f, indent=2)

def should_pause_wealth(cash, config):
    return cash < config.get("min_cash_buffer", 500)

def get_target_etf_allocations(config, portfolio_value):
    targets = {}
    for etf, pct in config.get("target_allocation", {}).items():
        targets[etf] = round(portfolio_value * pct, 2)
    return targets

def needs_rebalance(current_holdings, targets, tolerance=0.05):
    warnings = {}
    for etf, target_value in targets.items():
        current_value = current_holdings.get(etf, 0)
        if abs(current_value - target_value) / target_value > tolerance:
            warnings[etf] = {
                "target": target_value,
                "actual": current_value
            }
    return warnings
