import logging
from backend.services.tradier_client import TradierClient
import backend.ml.ml_scoring as ml_scoring

logger = logging.getLogger(__name__)
_tradier = TradierClient()

class TradeReplicationBot:
    def __init__(self, source_trade: dict, target_tickers: list[str], user_settings: dict):
        self.source_trade = source_trade
        self.target_tickers = target_tickers
        self.user_settings = user_settings
        self.replication_log: list = []

    def replicate(self) -> list:
        results = []
        for target in self.target_tickers:
            if not self._should_replicate_to(target):
                continue

            replicated_trade = self._build_trade_for_target(target)
            if not replicated_trade:
                continue

            score = score_trade(replicated_trade)
            if score < self.user_settings.get("min_score", 0.5):
                logger.warning(f"[ReplicationBot] Skipped {target} due to low score {score:.2f}")
                continue

            try:
                result = _tradier.place_order(**replicated_trade)
                logger.info(f"[ReplicationBot] Executed trade on {target}: {result}")
                self.replication_log.append(result)
                results.append(result)
            except Exception as e:
                logger.error(f"[ReplicationBot] Failed to replicate to {target}: {e}")
        return results

    def _should_replicate_to(self, target: str) -> bool:
        if target == self.source_trade["ticker"]:
            return False

    def _build_trade_for_target(self, target: str) -> dict | None:
        try:
            qty = min(
                self.source_trade.get("qty", 0),
                self.user_settings.get("max_qty_per_ticker", 5),
            )
            return {
                "account_id": self.source_trade["account_id"],
                "symbol":     target,
                "quantity":   qty,
                "strategy":   self.source_trade["strategy"],
            }
        except Exception as e:
            logger.error(f"[ReplicationBot] Error building trade for {target}: {e}")
            return None
