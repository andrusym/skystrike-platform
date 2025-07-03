
# wealth_projection_tool.py

import datetime

class WealthProjectionTool:
    def __init__(self, start_balance, monthly_contrib, annual_return_pct, goal_amount):
        self.start_balance = start_balance
        self.monthly_contrib = monthly_contrib
        self.annual_return_pct = annual_return_pct
        self.goal_amount = goal_amount

    def project(self, years=10):
        results = []
        balance = self.start_balance
        r = self.annual_return_pct / 12

        for month in range(1, years * 12 + 1):
            balance = balance * (1 + r) + self.monthly_contrib
            results.append({
                "month": month,
                "balance": round(balance, 2),
                "date": (datetime.datetime.today() + datetime.timedelta(days=30 * month)).strftime('%Y-%m')
            })
            if balance >= self.goal_amount:
                break

        return results
