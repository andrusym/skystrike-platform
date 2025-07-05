import logging
from backend.utils.database import get_strategy_run_data, flag_strategy

logger = logging.getLogger(__name__)

class StrategyBurnoutDetector:
    def __init__(self, threshold_days: int = 5, min_win_rate: float = 0.4):
        self.threshold_days = threshold_days
        self.min_win_rate = min_win_rate

    def evaluate(self, strategy_id: str) -> bool:
        data = get_strategy_run_data(strategy_id)
        if (
            data.get("consecutive_days", 0) >= self.threshold_days
            and data.get("win_rate", 1.0) < self.min_win_rate
        ):
            flag_strategy(strategy_id, reason="burnout")
            logger.warning(f"[BurnoutDetector] Strategy {strategy_id} flagged for burnout.")
            return True
        return False
