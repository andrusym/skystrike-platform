
# strategy_cooldown_engine.py

import logging
from backend.utils.database import log_cooldown, check_recent_trades

class StrategyCooldownEngine:
    def __init__(self, cooldown_threshold=3, cooldown_minutes=30):
        self.cooldown_threshold = cooldown_threshold
        self.cooldown_minutes = cooldown_minutes

    def check_and_enforce(self, strategy_id):
        recent_trades = check_recent_trades(strategy_id)
        if len(recent_trades) >= self.cooldown_threshold:
            log_cooldown(strategy_id, self.cooldown_minutes)
            logging.warning(f"[CooldownEngine] Cooling down {strategy_id} for {self.cooldown_minutes} minutes.")
            return True
        return False

def check_and_apply_cooldowns():
    """
    Placeholder cooldown logic for bots that may be trading too frequently.
    """
    from backend.utils.strategy_loader import get_all_bot_names
    from backend.utils.database import check_recent_trades, log_cooldown

    bots = get_all_bot_names()
    for bot in bots:
        if check_recent_trades(bot):
            log_cooldown(bot, "Too many recent trades – entering cooldown mode.")
    print("✅ Cooldown check complete.")
