# strategy_cooldown.py
from datetime import datetime, timedelta

cooldowns = {}

def should_pause_strategy(strategy_name):
    now = datetime.now()
    if strategy_name in cooldowns:
        if now < cooldowns[strategy_name]:
            return True
    return False

def apply_cooldown(strategy_name, days=1):
    cooldowns[strategy_name] = datetime.now() + timedelta(days=days)
