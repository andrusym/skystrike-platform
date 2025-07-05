import os
from typing import Dict, List, Literal, Optional
from backend.services.tradier_client import TradierClient

async def submit_multileg_order(
    account_id: str,
    legs: List[Dict],
    price: Optional[float] = None,
    order_type: Literal["market", "debit", "credit", "even"] = "market",
    duration: Literal["day", "gtc"] = "day",
    tag: str = "skystrike"
) -> Dict:
    client = TradierClient()
    payload = {
        "class": "multileg",
        "type": order_type,
        "duration": duration,
        "tag": tag,
        "price": price,
        "legs": legs,
    }
    return client.place_order(account_id, payload)

async def submit_option_order(
    account_id: str,
    option_symbol: str,
    quantity: int,
    side: Literal["buy_to_open", "sell_to_open", "buy_to_close", "sell_to_close"],
    price: Optional[float] = None,
    order_type: Literal["market", "limit", "stop", "stop_limit"] = "market",
    duration: Literal["day", "gtc"] = "day",
    tag: str = "skystrike"
) -> Dict:
    client = TradierClient()
    payload = {
        "class": "option",
        "type": order_type,
        "duration": duration,
        "tag": tag,
        "price": price,
        "option_symbol": option_symbol,
        "side": side,
        "quantity": quantity,
    }
    return client.place_order(account_id, payload)

async def submit_equity_order(
    account_id: str,
    symbol: str,
    quantity: int,
    side: Literal["buy", "sell"],
    order_type: Literal["market", "limit", "stop", "stop_limit"] = "market",
    duration: Literal["day", "gtc"] = "day",
    tag: str = "skystrike"
) -> Dict:
    client = TradierClient()
    payload = {
        "class": "equity",
        "type": order_type,
        "duration": duration,
        "tag": tag,
        "symbol": symbol,
        "side": side,
        "quantity": quantity,
    }
    return client.place_order(account_id, payload)
