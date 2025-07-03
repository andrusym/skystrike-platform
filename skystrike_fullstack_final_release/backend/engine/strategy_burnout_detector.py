
# strategy_burnout_detector.py

import logging
utils.database import get_strategy_run_data, flag_strategy

class StrategyBurnoutDetector:
    def __init__(self, threshold_days=5, min_win_rate=0.4):
        self.threshold_days = threshold_days
        self.min_win_rate = min_win_rate

    def evaluate(self, strategy_id):
        data = get_strategy_run_data(strategy_id)
        if data['consecutive_days'] >= self.threshold_days and data['win_rate'] < self.min_win_rate:
            flag_strategy(strategy_id, reason="burnout")
            logging.warning(f"[BurnoutDetector] Strategy {strategy_id} flagged for burnout.")
            return True
        return False
