
# tax_aware_rebalancer.py

import logging
from datetime import datetime
utils.database import get_holdings, get_tax_lots, place_tax_optimal_trades

class TaxAwareRebalancer:
    def __init__(self, user_id, tax_year=None):
        self.user_id = user_id
        self.tax_year = tax_year or datetime.today().year

    def rebalance(self):
        holdings = get_holdings(self.user_id)
        tax_lots = get_tax_lots(self.user_id, self.tax_year)

        trades_to_execute = []
        for asset in holdings:
            lots = tax_lots.get(asset['ticker'], [])
            for lot in lots:
                if lot['unrealized_gain'] < 0 and lot['holding_period'] > 365:
                    # Example: harvest long-term losses
                    trades_to_execute.append({
                        "action": "sell",
                        "ticker": asset['ticker'],
                        "quantity": lot['quantity'],
                        "reason": "Tax-loss harvesting"
                    })

        if trades_to_execute:
            place_tax_optimal_trades(self.user_id, trades_to_execute)
            logging.info(f"[TaxAwareRebalancer] Executed {len(trades_to_execute)} tax-optimal trades.")
        else:
            logging.info("[TaxAwareRebalancer] No tax-loss harvesting opportunities found.")
