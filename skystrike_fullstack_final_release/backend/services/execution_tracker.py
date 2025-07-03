"""
Tracks and logs execution details for post-trade analysis and slippage metrics.
"""
class ExecutionTracker:
    def __init__(self):
        self.logs = []

    def log_execution(self, order_id, symbol, qty, fill_price, expected_price):
        slippage = fill_price - expected_price
        self.logs.append({
            "order_id": order_id,
            "symbol": symbol,
            "qty": qty,
            "fill_price": fill_price,
            "expected_price": expected_price,
            "slippage": slippage
        })

    def get_slippage_report(self):
        return self.logs
