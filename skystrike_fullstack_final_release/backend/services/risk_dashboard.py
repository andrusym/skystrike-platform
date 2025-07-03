"""
Provides detailed exposure and risk metrics for the full portfolio.
"""
class RiskDashboard:
    def __init__(self):
        self.metrics = {}

    def update_metrics(self, positions):
        self.metrics = {
            "total_delta": sum(p.get("delta", 0) for p in positions),
            "total_gamma": sum(p.get("gamma", 0) for p in positions),
            "vega_exposure": sum(p.get("vega", 0) for p in positions),
            "theta_decay": sum(p.get("theta", 0) for p in positions)
        }
        return self.metrics
