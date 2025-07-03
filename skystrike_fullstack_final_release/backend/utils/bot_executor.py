# utils/bot_executor.py

import importlib
import traceback

utils.trade_logger import log_trade

def run_bot(bot_name: str, ticker: str = "SPY", contracts: int = 1):
    """
    Dynamically import and run a bot strategy.
    Looks for bot modules inside bots/ directory, each exposing a run() method.
    """
    try:
        module_path = f"backend.bots.{bot_name}"
        bot_module = importlib.import_module(module_path)

        if hasattr(bot_module, "run"):
            result = bot_module.run(ticker=ticker, contracts=contracts)
            log_trade({
                "strategy": bot_name,
                "ticker": ticker,
                "contracts": contracts,
                "status": "TRIGGERED",
                "result": result
            })
            return {"success": True, "message": f"{bot_name} triggered successfully."}
        else:
            return {"success": False, "message": f"Bot module {bot_name} has no 'run' method."}
    except Exception as e:
        traceback.print_exc()
        return {
            "success": False,
            "message": f"Failed to run bot {bot_name}: {str(e)}"
        }
