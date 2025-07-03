
# volatility_surface_scanner.py

import numpy as np

class VolatilitySurfaceScanner:
    def __init__(self, iv_data):
        self.iv_data = iv_data  # Dictionary with strikes as keys, IVs as values

    def analyze(self):
        smile_score = self._calculate_smile_score()
        skew_score = self._calculate_skew_score()
        return {
            "smile": smile_score,
            "skew": skew_score,
            "is_valid": abs(smile_score) < 0.2 and abs(skew_score) < 0.3
        }

    def _calculate_smile_score(self):
        strikes = sorted(self.iv_data.keys())
        mids = np.array(strikes)[len(strikes)//3:-len(strikes)//3]
        mids_iv = [self.iv_data[s] for s in mids]
        center = np.mean(mids_iv)
        wings = [self.iv_data[strikes[0]], self.iv_data[strikes[-1]]]
        return np.mean(wings) - center

    def _calculate_skew_score(self):
        strikes = sorted(self.iv_data.keys())
        low, high = strikes[0], strikes[-1]
        return self.iv_data[high] - self.iv_data[low]
