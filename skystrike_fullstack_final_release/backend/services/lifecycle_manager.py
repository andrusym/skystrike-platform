"""
Lifecycle manager for strategies — handles retry, degrade, recycle logic.
"""
class LifecycleManager:
    def __init__(self):
        self.failed_strategies = {}

    def register_failure(self, strategy):
        self.failed_strategies[strategy] = self.failed_strategies.get(strategy, 0) + 1

    def should_retry(self, strategy):
        return self.failed_strategies.get(strategy, 0) < 3

    def reset(self, strategy):
        if strategy in self.failed_strategies:
            del self.failed_strategies[strategy]
