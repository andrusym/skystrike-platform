# drawdown_guard.py
MAX_DRAWDOWN = -1000

def should_degrade(performance_log):
    trailing_pnl = sum(performance_log[-5:])
    return trailing_pnl < MAX_DRAWDOWN
