from backend.services.tradier_client import TradierClient
import logging
async def build_order(ticker: str, contracts: int, dte: int, mode: str) -> dict:
    return {
        "class": "equity",
        "symbol": ticker,
        "side": "buy",
        "quantity": contracts,
        "price": None
    }
