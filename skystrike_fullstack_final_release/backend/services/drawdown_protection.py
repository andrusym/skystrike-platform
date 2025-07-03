
# drawdown_protection.py

import logging
utils.database import get_drawdown_data, throttle_strategy

class DrawdownProtection:
    def __init__(self, max_drawdown=-0.15):
        self.max_drawdown = max_drawdown

    def enforce(self, strategy_id):
        drawdown = get_drawdown_data(strategy_id)
        if drawdown < self.max_drawdown:
            throttle_strategy(strategy_id)
            logging.warning(f"[DrawdownProtection] Strategy {strategy_id} throttled due to drawdown: {drawdown}")
            return True
        return False
