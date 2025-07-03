"""
Evaluates gamma risk in option positions and issues risk alerts.
"""
class GammaRiskEvaluator:
    def __init__(self, threshold=5000):
        self.gamma_threshold = threshold

    def assess(self, gamma_exposure):
        return gamma_exposure > self.gamma_threshold
