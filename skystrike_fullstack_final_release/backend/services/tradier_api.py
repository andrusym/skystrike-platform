import os
import logging
from typing import List, Dict, Any, Optional
import requests

logger = logging.getLogger(__name__)

SANDBOX_BASE = "https://sandbox.tradier.com/v1"
LIVE_BASE = "https://api.tradier.com/v1"

def get_tradier_session(sandbox: bool = True) -> tuple[requests.Session, str, str]:
    token = (
        os.getenv("TRADIER_PAPER_ACCESS_TOKEN")
        if sandbox else os.getenv("TRADIER_LIVE_ACCESS_TOKEN")
    )
    if not token:
        raise ValueError("Must set TRADIER access token")

    account_id = (
        os.getenv("TRADIER_PAPER_ACCOUNT_ID")
        if sandbox else os.getenv("TRADIER_LIVE_ACCOUNT_ID")
    )
    if not account_id:
        raise ValueError("Must set TRADIER account ID")

    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    })

    return session, (SANDBOX_BASE if sandbox else LIVE_BASE), account_id


def _get(path: str, params: dict = None, sandbox: bool = True) -> dict:
    session, base, _ = get_tradier_session(sandbox)
    url = f"{base}{path}"
    r = session.get(url, params=params or {})
    r.raise_for_status()
    return r.json()


def _post(path: str, data: dict, sandbox: bool = True) -> dict:
    session, base, account_id = get_tradier_session(sandbox)
    url = f"{base}{path.format(account_id=account_id)}"
    print(f"[POST] URL: {url}")
    print(f"[POST] DATA: {data}")
    r = session.post(
        url,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    print(f"[POST] STATUS: {r.status_code}")
    try:
        print(f"[POST] RESPONSE: {r.json()}")
    except Exception:
        print(f"[POST] TEXT RESPONSE: {r.text}")
    r.raise_for_status()
    return r.json()


def get_expirations(symbol: str) -> List[str]:
    data = _get("/markets/options/expirations", {"symbol": symbol})
    return data.get("expirations", {}).get("date", [])


def get_quote(symbol: str) -> Dict[str, Any]:
    data = _get("/markets/quotes", {"symbols": symbol})
    return data.get("quotes", {}).get("quote", {})


def format_tradier_option_symbol(
    ticker: str, expiration: str, right: str, strike: float
) -> str:
    strike_formatted = f"{int(strike * 1000):08d}"
    return f"{ticker}{expiration}{right}{strike_formatted}"


def submit_option_order(
    option_symbol: str,
    side: str,
    quantity: int,
    price: Optional[float] = None
) -> dict:
    # extract the underlying symbol (everything before the 6-digit date + 1-char right + 8-digit strike)
    underlying = option_symbol[:-15]
    payload = {
        "class": "option",
        "symbol": underlying,
        "option_symbol": option_symbol,
        "side": side,
        "quantity": str(quantity),
        "duration": "day",
        "type": "market" if price is None else "limit",
    }
    if price is not None:
        payload["price"] = str(price)
    return _post("/accounts/{account_id}/orders", payload)


def submit_equity_order(
    symbol: str,
    side: str,
    quantity: int,
    price: Optional[float] = None
) -> dict:
    payload = {
        "class": "equity",
        "symbol": symbol,
        "side": side,
        "quantity": str(quantity),
        "duration": "day",
        "type": "market" if price is None else "limit",
    }
    if price is not None:
        payload["price"] = str(price)
    return _post("/accounts/{account_id}/orders", payload)


def submit_multileg_order(
    symbol: str,
    legs: List[Dict[str, Any]],
    price: float = 1.0
) -> dict:
    payload = {
        "class": "multileg",
        "type": "debit",  # debit for multileg orders
        "symbol": symbol,
        "duration": "day",
        "price": str(price)
    }
    for i, leg in enumerate(legs):
        payload[f"option_symbol[{i}]"] = leg["option_symbol"]
        payload[f"side[{i}]"] = leg["side"]
        qty = leg.get("quantity", 1)
        payload[f"quantity[{i}]"] = str(qty if qty else 1)
    return _post("/accounts/{account_id}/orders", payload)


def get_open_pnl(
    account_id: str = None,
    access_token: str = None,
    mode: str = "paper"
) -> float:
    if not account_id:
        account_id = os.getenv(
            "TRADIER_PAPER_ACCOUNT_ID"
            if mode == "paper"
            else "TRADIER_LIVE_ACCOUNT_ID"
        )
    if not access_token:
        access_token = os.getenv(
            "TRADIER_PAPER_ACCESS_TOKEN"
            if mode == "paper"
            else "TRADIER_LIVE_ACCESS_TOKEN"
        )

    url = f"{LIVE_BASE}/accounts/{account_id}/positions"
    if mode == "paper":
        url = url.replace(LIVE_BASE, SANDBOX_BASE)

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    positions = response.json().get("positions", {}).get("position", [])
    if not positions:
        return 0.0

    total_pnl = sum(float(p.get("gain_loss", 0.0)) for p in positions)
    return round(total_pnl, 2)


def get_open_orders(sandbox: bool = True) -> List[Dict[str, Any]]:
    session, base, account_id = get_tradier_session(sandbox)
    url = f"{base}/accounts/{account_id}/orders"
    r = session.get(url)
    r.raise_for_status()
    return r.json().get("orders", {}).get("order", [])


def fetch_order_status(order_id: str, sandbox: bool = True) -> dict:
    session, base, account_id = get_tradier_session(sandbox)
    url = f"{base}/accounts/{account_id}/orders/{order_id}"
    response = session.get(url)
    response.raise_for_status()
    return response.json()
