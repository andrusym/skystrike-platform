import os
import httpx
from datetime import date, timedelta
from dotenv import load_dotenv

load_dotenv()

TRADIER_TOKEN = os.getenv(f"TRADIER_{TRADIER_MODE.upper()}_ACCESS_TOKEN")
TRADIER_ACCOUNT_ID = os.getenv(f"TRADIER_{TRADIER_MODE.upper()}_ACCOUNT_ID")


async def run_bot_with_params(ticker: str, contracts: int, dte: int, price: float | None = None, confidence: float | None = None):
    """
    Submit a 4-leg Iron Condor order via Tradier (multileg market or limit order).

    Args:
        ticker (str): Underlying symbol.
        contracts (int): Number of contracts.
        dte (int): Days to expiration.
        price (float | None): Optional limit price; if None, submit market order.
        confidence (float | None): Optional ML confidence score to add as a tag.

    Returns:
        dict: Tradier API JSON response.
    """

    # Build expiration string
    today = date.today()
    target_exp = today + timedelta(days=dte)
    exp_str = target_exp.strftime("%y%m%d")

    # Define ATM and leg strikes
    width = 5
    atm = round(contracts / width) * width

    strikes = {
        0: (atm + width,   "C", "sell_to_open"),
        1: (atm + 2*width, "C", "buy_to_open"),
        2: (atm - width,   "P", "sell_to_open"),
        3: (atm - 2*width, "P", "buy_to_open"),
    }

    # Determine order type and price field
    order_type = "limit" if price is not None else "market"
    order_price = f"{price:.2f}" if price is not None else "1.00"  # Tradier requires price for multileg even market

    # Build payload according to Tradier multileg spec
    data = {
        "class": "multileg",
        "type": order_type,
        "symbol": ticker,
        "duration": "day",
        "price": order_price,
    }

    # Add ML confidence tag if provided
    if confidence is not None:
        data["tag"] = f"confidence_{round(confidence, 2)}"

    for i, (strike, right, side) in strikes.items():
        s = f"{int(strike * 1000):08d}"
        option_symbol = f"{ticker}{exp_str}{right}{s}"
        data[f"option_symbol[{i}]"] = option_symbol
        data[f"side[{i}]"] = side
        data[f"quantity[{i}]"] = contracts

    # Log the outgoing payload
    print("\n[TRADIER ORDER REQUEST PAYLOAD]")
    for k in sorted(data.keys()):
        print(f"{k}: {data[k]}")

    async with httpx.AsyncClient(
        base_url=TRADIER_BASE_URL,
        headers={
            "Authorization": f"Bearer {TRADIER_TOKEN}",
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        timeout=30.0,
    ) as client:
        resp = await client.post(
            f"/accounts/{TRADIER_ACCOUNT_ID}/orders",
            data=data,
        )

        print("\n[TRADIER RESPONSE]")
        print(f"Status Code: {resp.status_code}")
        print(f"Response Body:\n{resp.text}")

        try:
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise RuntimeError(f"Tradier error {resp.status_code}: {resp.text or str(exc)}")

        return resp.json()
