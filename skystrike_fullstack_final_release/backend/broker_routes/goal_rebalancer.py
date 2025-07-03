# goal_rebalancer.py
def calculate_rebalance(current_profit, monthly_goal, etf_alloc):
    if current_profit >= monthly_goal:
        # shift from growth to bonds
        return {"VOO": 30, "BND": 50, "VXUS": 20}
    else:
        # keep growth-heavy
        return etf_alloc
