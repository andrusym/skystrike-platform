"""
Implements basic tax-aware rebalancing logic.
"""
class TaxRebalancer:
    def __init__(self):
        self.cap_gains_threshold = 10000  # USD

    def should_rebalance(self, capital_gains):
        return capital_gains > self.cap_gains_threshold
