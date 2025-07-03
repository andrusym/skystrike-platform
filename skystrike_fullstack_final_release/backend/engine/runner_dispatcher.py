# backend/engine/runner_dispatcher.py

from backend.engine.bot_entry_engine import execute_bot

def dispatch_bot_by_name(name: str, ticker: str = None, contracts: int = 1, context: list = None):
    """
    Central dispatcher to call any registered bot by name.
    """
    return execute_bot(name=name, ticker=ticker, contracts=contracts, context=context or [])
