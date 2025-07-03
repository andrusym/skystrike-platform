
# etf_auto_rotation.py

import logging
utils.market_data import get_macro_signals
utils.broker_api import rotate_etfs

class ETFMacroRotator:
    def __init__(self, portfolio):
        self.portfolio = portfolio

    def rotate(self):
        signals = get_macro_signals()
        target_allocation = self._determine_rotation(signals)

        try:
            rotate_etfs(self.portfolio, target_allocation)
            logging.info(f"[ETFMacroRotator] Rotated to {target_allocation}")
            return target_allocation
        except Exception as e:
            logging.error(f"[ETFMacroRotator] Rotation failed: {e}")
            return None

    def _determine_rotation(self, signals):
        if signals['risk_off']:
            return {'TLT': 0.5, 'GLD': 0.3, 'CASH': 0.2}
        elif signals['risk_on']:
            return {'SPY': 0.4, 'QQQ': 0.4, 'XLF': 0.2}
        return {'CASH': 1.0}
