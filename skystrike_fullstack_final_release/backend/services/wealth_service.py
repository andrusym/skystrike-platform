# This would load ETF/cash state from the wealth engine
def get_wealth_summary():
    return {
        "cash": 20000,
        "etfs": {
            "VTI": {"shares": 15, "value": 3600},
            "SPY": {"shares": 5, "value": 2700}
        }
    }
