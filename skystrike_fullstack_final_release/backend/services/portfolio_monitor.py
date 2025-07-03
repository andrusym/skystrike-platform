"""
Monitors correlation between active strategies and manages diversification risk.
"""
import numpy as np

class PortfolioMonitor:
    def __init__(self):
        self.correlation_threshold = 0.85  # Default threshold

    def compute_correlation_matrix(self, strategy_returns: dict):
        # strategy_returns: {strategy_name: [returns]}
        data = [returns for returns in strategy_returns.values()]
        if len(data) < 2:
            return None
        return np.corrcoef(data)

    def is_portfolio_overlapping(self, correlation_matrix):
        if correlation_matrix is None:
            return False
        upper_tri = correlation_matrix[np.triu_indices(len(correlation_matrix), k=1)]
        return any(corr > self.correlation_threshold for corr in upper_tri)
