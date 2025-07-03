
# trade_replication_bot.py

import logging
utils.broker_api import execute_trade
utils.ml_scoring import score_trade
from config import REPLICATION_CONFIG

class TradeReplicationBot:
    def __init__(self, source_trade, target_tickers, user_settings):
        self.source_trade = source_trade  # dict with fields like 'ticker', 'strategy', 'legs', 'qty'
        self.target_tickers = target_tickers  # list of tickers to replicate to
        self.user_settings = user_settings  # e.g., max position per ticker, strategy type
        self.replication_log = []

    def replicate(self):
        logging.info(f"[ReplicationBot] Starting replication from: {self.source_trade['ticker']}")
        results = []

        for target in self.target_tickers:
            if not self._should_replicate_to(target):
                continue

            replicated_trade = self._build_trade_for_target(target)
            if not replicated_trade:
                continue

            score = score_trade(replicated_trade)
            if score < self.user_settings.get("min_score", 0.5):
                logging.warning(f"[ReplicationBot] Skipped {target} due to low ML score ({score:.2f})")
                continue

            try:
                result = execute_trade(replicated_trade)
                logging.info(f"[ReplicationBot] Executed trade on {target}: {result}")
                self.replication_log.append(result)
                results.append(result)
            except Exception as e:
                logging.error(f"[ReplicationBot] Failed to replicate to {target}: {e}")

        return results

    def _should_replicate_to(self, target):
        if target == self.source_trade["ticker"]:
            return False
        if target not in REPLICATION_CONFIG.get("approved_tickers", []):
            return False
        return True

    def _build_trade_for_target(self, target):
        try:
            legs = self.source_trade["legs"]
            strategy = self.source_trade["strategy"]
            qty = min(self.source_trade["qty"], self.user_settings.get("max_qty_per_ticker", 5))

            return {
                "ticker": target,
                "strategy": strategy,
                "legs": legs,  # assumed to be re-priced elsewhere
                "qty": qty
            }
        except Exception as e:
            logging.error(f"[ReplicationBot] Error building trade for {target}: {e}")
            return None
