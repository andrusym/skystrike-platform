"""
Handles trade execution logic, triggered from ML recommendations or user actions.
"""

from backend.broker.submit_order import run_bot_with_params

def execute_trade(bot: str, ticker: str, contracts: int, dte: int = 0):
    """
    Execute a trade using the specified bot and parameters.
    """
    print(f"🚀 Executing trade: bot={bot}, ticker={ticker}, contracts={contracts}, dte={dte}")
    return run_bot_with_params(bot_name=bot, ticker=ticker, contracts=contracts, dte=dte)
