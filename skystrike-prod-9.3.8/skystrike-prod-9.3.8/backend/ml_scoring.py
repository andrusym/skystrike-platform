
import numpy as np
import datetime
import random

class StrategyScorer:
    def __init__(self):
        self.model_version = "v1.3.2"
        self.strategy_memory = {}

    def score_strategy(self, ticker, strategy_type):
        now = datetime.datetime.utcnow().isoformat()
        features = self._extract_features(ticker, strategy_type)
        score = self._ml_model_predict(features)
        self._record_score(ticker, strategy_type, score, now)
        return round(score, 4)

    def _extract_features(self, ticker, strategy_type):
        # Simulate feature extraction
        iv_rank = np.random.normal(0.5, 0.15)
        vix_level = np.random.normal(18, 5)
        volume_score = np.random.uniform(0, 1)
        recent_pnl = np.random.normal(0.02, 0.01)
        strategy_hit_rate = np.random.uniform(0.6, 0.95)
        return {
            "ticker": ticker,
            "strategy": strategy_type,
            "iv_rank": iv_rank,
            "vix_level": vix_level,
            "volume_score": volume_score,
            "recent_pnl": recent_pnl,
            "hit_rate": strategy_hit_rate
        }

    def _ml_model_predict(self, features):
        base = features["hit_rate"] * 0.5 + features["volume_score"] * 0.3
        base += 0.1 if features["iv_rank"] < 0.4 else -0.1
        noise = np.random.normal(0, 0.05)
        score = min(1.0, max(0.0, base + noise))
        return score

    def _record_score(self, ticker, strategy, score, timestamp):
        if ticker not in self.strategy_memory:
            self.strategy_memory[ticker] = []
        self.strategy_memory[ticker].append({
            "strategy": strategy,
            "score": score,
            "timestamp": timestamp
        })

    def get_recent_scores(self, ticker, limit=5):
        if ticker not in self.strategy_memory:
            return []
        return self.strategy_memory[ticker][-limit:]

    def average_score(self, ticker):
        if ticker not in self.strategy_memory or not self.strategy_memory[ticker]:
            return 0.0
        scores = [entry["score"] for entry in self.strategy_memory[ticker]]
        return round(sum(scores) / len(scores), 4)
