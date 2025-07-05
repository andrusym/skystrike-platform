import logging
from backend.utils.database import (
    get_paused_strategies,
    score_strategy,
    reprice_trade,
    reenter_trade,
)

logger = logging.getLogger(__name__)

class StrategyReentryLogic:
    def __init__(self, min_score_threshold: float = 0.6):
        self.min_score = min_score_threshold

    def evaluate_reentries(self) -> None:
        paused = get_paused_strategies()
        for strategy in paused:
            score = score_strategy(strategy)
            if score >= self.min_score:
                new_trade = reprice_trade(strategy)
                result = reenter_trade(new_trade)
                logger.info(f"[ReentryLogic] Reentered {strategy} with new trade: {result}")
