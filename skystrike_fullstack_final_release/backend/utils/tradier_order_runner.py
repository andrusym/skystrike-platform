# backend/utils/tradier_order_runner.py

import os
from dotenv import load_dotenv
import httpx
from datetime import date, timedelta
from typing import List, Dict, Any

# Load .env from project root
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path=env_path, override=True)

TRADIER_TOKEN      = os.getenv(f"TRADIER_{TRADIER_MODE.upper()}_ACCESS_TOKEN")
TRADIER_ACCOUNT_ID = os.getenv(f"TRADIER_{TRADIER_MODE.upper()}_ACCOUNT_ID")

HEADERS = {
    "Authorization": f"Bearer {TRADIER_TOKEN}",
    "Accept":        "application/json",
}


# -- Helpers --

async def get_underlying_price(symbol: str) -> float:
    """Fetch the last trade price of the underlying."""
    url = f"{TRADIER_BASE_URL}/markets/quotes?symbols={symbol}"
    async with httpx.AsyncClient(headers=HEADERS, timeout=10.0) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        jd = resp.json() or {}
        quotes = jd.get("quotes") or {}
        quote = quotes.get("quote")
        if not quote:
            raise ValueError(f"No quote data for {symbol}: {jd}")
        q = quote[0] if isinstance(quote, list) else quote
        last = q.get("last")
        if last is None:
            raise ValueError(f"Quote missing 'last' for {symbol}: {q}")
        return float(last)


async def get_option_chain(symbol: str, expiration: str) -> List[Dict[str, Any]]:
    """
    Fetch the option chain for a given expiration (YYMMDD).
    Returns a list of option dicts, or [] if none found.
    """
    url = f"{TRADIER_BASE_URL}/markets/options/chains?symbol={symbol}&expiration={expiration}"
    async with httpx.AsyncClient(headers=HEADERS, timeout=20.0) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        jd = resp.json() or {}
        opts_container = jd.get("options") or {}
        opts = opts_container.get("option")
        if not opts:
            return []
        return opts if isinstance(opts, list) else [opts]


def extract_strikes(chain: List[Dict[str, Any]]) -> List[float]:
    """
    Pull out unique strike prices as floats, sorted ascending.
    Skips any entries without a valid 'strike' field.
    """
    strikes = set()
    for o in chain or []:
        try:
            s = o.get("strike")
            if s is not None:
                strikes.add(float(s))
        except Exception:
            continue
    return sorted(strikes)


def select_strike(available: List[float], target: float, above: bool) -> float:
    """
    From a sorted list of strikes, pick the first strike >= target (if above=True),
    else the last strike <= target.
    """
    if not available:
        raise ValueError("No strikes available to select from")
    if above:
        for s in available:
            if s >= target:
                return s
        return available[-1]
    else:
        for s in reversed(available):
            if s <= target:
                return s
        return available[0]


# -- Order runners --

async def run_multileg_order(
    symbol: str,
    legs: List[dict],
    order_type: str = "market",
    price: str = "1.00",
    duration: str = "day",
    tag: str = None
) -> Dict[str, Any]:
    data = {
        "class":    "multileg",
        "symbol":   symbol,
        "type":     order_type,
        "duration": duration,
        "price":    price
    }
    if tag:
        data["tag"] = tag

    for idx, leg in enumerate(legs or []):
        data[f"option_symbol[{idx}]"] = leg["option_symbol"]
        data[f"side[{idx}]"]          = leg["side"]
        data[f"quantity[{idx}]"]      = str(leg["quantity"])

    async with httpx.AsyncClient(base_url=TRADIER_BASE_URL, headers=HEADERS, timeout=30.0) as client:
        resp = await client.post(f"/accounts/{TRADIER_ACCOUNT_ID}/orders", data=data)
        resp.raise_for_status()
        return {"legs": legs, **resp.json()}


async def run_option_order(
    symbol: str,
    leg: dict,
    order_type: str = "market",
    duration: str = "day",
    price: str = None,
    stop: str = None,
    tag: str = None
) -> Dict[str, Any]:
    data = {
        "class":         "option",
        "symbol":        symbol,
        "option_symbol": leg["option_symbol"],
        "side":          leg["side"],
        "quantity":      str(leg["quantity"]),
        "type":          order_type,
        "duration":      duration
    }
    if price: data["price"] = price
    if stop:  data["stop"]  = stop
    if tag:   data["tag"]   = tag

    async with httpx.AsyncClient(base_url=TRADIER_BASE_URL, headers=HEADERS, timeout=30.0) as client:
        resp = await client.post(f"/accounts/{TRADIER_ACCOUNT_ID}/orders", data=data)
        resp.raise_for_status()
        return {"legs": [leg], **resp.json()}


async def run_equity_order(
    symbol: str,
    side: str,
    quantity: int,
    order_type: str = "market",
    duration: str = "day",
    price: str = None,
    stop: str = None,
    tag: str = None
) -> Dict[str, Any]:
    data = {
        "class":    "equity",
        "symbol":   symbol,
        "side":     side,
        "quantity": str(quantity),
        "type":     order_type,
        "duration": duration
    }
    if price: data["price"] = price
    if stop:  data["stop"]  = stop
    if tag:   data["tag"]   = tag

    async with httpx.AsyncClient(base_url=TRADIER_BASE_URL, headers=HEADERS, timeout=30.0) as client:
        resp = await client.post(f"/accounts/{TRADIER_ACCOUNT_ID}/orders", data=data)
        resp.raise_for_status()
        return {"legs": [], **resp.json()}


async def run_bot_with_params(
    strategy: str,
    ticker: str,
    contracts: int,
    dte: int
) -> Dict[str, Any]:
    """
    Build an ATM-based order using real, available strikes.
    """
    exp_str = (date.today() + timedelta(days=dte)).strftime("%y%m%d")

    # fetch price & chain
    underlying = await get_underlying_price(ticker)
    chain      = await get_option_chain(ticker, exp_str)
    if not chain:
        raise ValueError(f"No option chain for {ticker} exp={exp_str}")

    strikes = extract_strikes(chain)
    if not strikes:
        raise ValueError(f"No valid strikes extracted for {ticker} exp={exp_str}")

    # compute ATM
    width      = 5.0
    atm_target = round(underlying / width) * width

    # select
    call1 = select_strike(strikes, atm_target + width,  above=True)
    call2 = select_strike(strikes, atm_target + 2*width,above=True)
    put1  = select_strike(strikes, atm_target - width,  above=False)
    put2  = select_strike(strikes, atm_target - 2*width,above=False)

    # build & submit
    if strategy in ("ironcondor", "kingcondor"):
        legs = [
            {"option_symbol": f"{ticker}{exp_str}C{int(call1*1000):08d}",
             "side":"sell_to_open", "quantity":contracts},
            {"option_symbol": f"{ticker}{exp_str}C{int(call2*1000):08d}",
             "side":"buy_to_open",  "quantity":contracts},
            {"option_symbol": f"{ticker}{exp_str}P{int(put1*1000):08d}",
             "side":"sell_to_open", "quantity":contracts},
            {"option_symbol": f"{ticker}{exp_str}P{int(put2*1000):08d}",
             "side":"buy_to_open",  "quantity":contracts},
        ]
        return await run_multileg_order(ticker, legs)

    elif strategy == "spread":
        legs = [
            {"option_symbol": f"{ticker}{exp_str}C{int(call1*1000):08d}",
             "side":"sell_to_open", "quantity":contracts},
            {"option_symbol": f"{ticker}{exp_str}C{int(call2*1000):08d}",
             "side":"buy_to_open",  "quantity":contracts},
        ]
        return await run_multileg_order(ticker, legs, price="0.50")

    elif strategy in ("csp", "wheel", "trend"):
        leg = {
            "option_symbol": f"{ticker}{exp_str}P{int(put1*1000):08d}",
            "side":           "sell_to_open",
            "quantity":       contracts
        }
        return await run_option_order(ticker, leg)

    elif strategy == "buyqqq":
        return await run_equity_order("QQQ", side="buy", quantity=contracts)

    else:
        raise ValueError(f"Unknown strategy: {strategy}")


async def run_all_bots() -> Dict[str, Any]:
    strategies = ["ironcondor","kingcondor","spread","csp","wheel","trend","buyqqq"]
    results: Dict[str, Any] = {}
    for strat in strategies:
        try:
            results[strat] = await run_bot_with_params(strat, ticker="SPY", contracts=1, dte=0)
        except Exception as e:
            results[strat] = {"error": str(e)}
    return results
