"""
Capital allocation engine for smart scaling based on strategy performance.
"""
class CapitalAllocator:
    def __init__(self, total_capital):
        self.total_capital = total_capital

    def allocate(self, strategy_scores):
        total_score = sum(strategy_scores.values())
        return {
            strategy: (score / total_score) * self.total_capital
            for strategy, score in strategy_scores.items()
        } if total_score else {strategy: 0 for strategy in strategy_scores}
