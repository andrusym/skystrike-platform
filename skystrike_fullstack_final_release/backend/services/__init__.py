from backend.bots.base import TradierClient

_client = TradierClient()

async def get_expirations(symbol: str):
    return _client.get_expirations(symbol)

async def get_quote(symbol: str):
    return _client.get_quote(symbol)

format_tradier_option_symbol = _client.format_option

async def submit_multileg_order(symbol: str, legs: list, price: float = 1.0):
    return _client.submit_multileg(symbol, legs, price)

async def submit_equity_order(symbol: str, side: str, quantity: int):
    return _client.submit_equity(symbol, side, quantity)

async def submit_option_order(option_symbol: str, side: str, quantity: int):
    return _client.submit_option(option_symbol, side, quantity)
