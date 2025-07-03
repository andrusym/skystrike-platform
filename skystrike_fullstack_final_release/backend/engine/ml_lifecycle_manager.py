
# ml_lifecycle_manager.py

import logging
utils.database import get_bot_performance, deactivate_bot, reactivate_bot

class MLLifecycleManager:
    def __init__(self, performance_thresholds):
        self.thresholds = performance_thresholds  # e.g., {'min_win_rate': 0.55, 'max_drawdown': -0.15}

    def evaluate_bots(self, bot_list):
        results = []

        for bot in bot_list:
            perf = get_bot_performance(bot)
            logging.info(f"[LifecycleManager] Evaluating {bot}: {perf}")

            if perf['win_rate'] < self.thresholds['min_win_rate'] or perf['drawdown'] < self.thresholds['max_drawdown']:
                deactivate_bot(bot)
                results.append((bot, 'deactivated'))
                logging.warning(f"[LifecycleManager] Deactivated {bot} due to underperformance.")
            elif not perf['active'] and perf['win_rate'] >= self.thresholds['min_win_rate']:
                reactivate_bot(bot)
                results.append((bot, 'reactivated'))
                logging.info(f"[LifecycleManager] Reactivated {bot} after recovery.")
            else:
                results.append((bot, 'no_change'))

        return results
