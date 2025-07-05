import logging
from backend.utils.database import get_bot_performance, deactivate_bot, reactivate_bot

logger = logging.getLogger(__name__)

class MLLifecycleManager:
    def __init__(self, performance_thresholds: dict):
        self.thresholds = performance_thresholds

    def evaluate_bots(self, bot_list: list[str]) -> list[tuple[str, str]]:
        results = []
        for bot in bot_list:
            perf = get_bot_performance(bot)
            logger.info(f"[LifecycleManager] Evaluating {bot}: {perf}")
            if perf.get("win_rate", 1) < self.thresholds.get("min_win_rate", 0) or perf.get("drawdown", 0) < self.thresholds.get("max_drawdown", 0):
                deactivate_bot(bot)
                results.append((bot, "deactivated"))
                logger.warning(f"[LifecycleManager] Deactivated {bot}.")
            elif not perf.get("active") and perf.get("win_rate", 0) >= self.thresholds.get("min_win_rate", 0):
                reactivate_bot(bot)
                results.append((bot, "reactivated"))
                logger.info(f"[LifecycleManager] Reactivated {bot}.")
            else:
                results.append((bot, "no_change"))
        return results
