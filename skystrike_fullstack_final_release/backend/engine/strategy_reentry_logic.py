
# strategy_reentry_logic.py

import logging
utils.database import get_paused_strategies, score_strategy, reprice_trade, reenter_trade

class StrategyReentryLogic:
    def __init__(self, min_score_threshold=0.6):
        self.min_score = min_score_threshold

    def evaluate_reentries(self):
        paused = get_paused_strategies()
        for strategy in paused:
            score = score_strategy(strategy)
            if score >= self.min_score:
                new_trade = reprice_trade(strategy)
                result = reenter_trade(new_trade)
                logging.info(f"[ReentryLogic] Reentered {strategy} with new trade: {result}")
