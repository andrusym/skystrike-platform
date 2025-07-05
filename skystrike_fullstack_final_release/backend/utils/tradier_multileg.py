import os
import httpx
from datetime import date, timedelta
from dotenv import load_dotenv

load_dotenv()

TRADIER_TOKEN = (
    os.getenv(f"TRADIER_{TRADIER_MODE.upper()}_ACCESS_TOKEN")
    or os.getenv("TRADIER_API_KEY")
)
TRADIER_ACCOUNT_ID = (
    os.getenv(f"TRADIER_{TRADIER_MODE.upper()}_ACCOUNT_ID")
    or os.getenv("TRADIER_ACCOUNT_ID")
)


async def run_bot_with_params(ticker: str, contracts: int, dte: int, legs: dict) -> dict:
    """
    Submit a multileg order to Tradier.
    
    Args:
        ticker: Underlying ticker symbol, e.g. "SPY"
        contracts: Number of contracts per leg
        dte: Days to expiration
        legs: dict mapping leg index to tuple(strike(float), right('C' or 'P'), side(str))
              e.g. {
                0: (strike1, "C", "sell_to_open"),
                1: (strike2, "C", "buy_to_open"),
                ...
              }
    """
    exp_date = date.today() + timedelta(days=dte)
    exp_str = exp_date.strftime("%y%m%d")

    data = {
        "class": "multileg",
        "symbol": ticker,
        "type": "market",
        "duration": "day",
        "price": "1.00",
    }

    for i, (strike, right, side) in legs.items():
        strike_formatted = f"{int(strike * 1000):08d}"
        data[f"option_symbol[{i}]"] = f"{ticker}{exp_str}{right}{strike_formatted}"
        data[f"side[{i}]"] = side
        data[f"quantity[{i}]"] = contracts

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
        resp = await client.post(f"/accounts/{TRADIER_ACCOUNT_ID}/orders", data=data)

        print("\n[TRADIER RESPONSE]")
        print(f"Status Code: {resp.status_code}")
        print(f"Response Body:\n{resp.text}")

        try:
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise RuntimeError(f"Tradier error {resp.status_code}: {resp.text or str(exc)}")

        return resp.json()

# === Example usage ===
# Iron Condor legs definition:
iron_condor_legs = {
    0: (300.0, "C", "sell_to_open"),
    1: (305.0, "C", "buy_to_open"),
    2: (290.0, "P", "sell_to_open"),
    3: (285.0, "P", "buy_to_open"),
}

# King Condor legs definition (example - adjust strikes as needed):
king_condor_legs = {
    0: (300.0, "C", "sell_to_open"),
    1: (305.0, "C", "buy_to_open"),
    2: (310.0, "C", "sell_to_open"),
    3: (315.0, "C", "buy_to_open"),
    4: (290.0, "P", "sell_to_open"),
    5: (285.0, "P", "buy_to_open"),
    6: (280.0, "P", "sell_to_open"),
    7: (275.0, "P", "buy_to_open"),
}

# To submit an order:
# await run_bot_with_params("SPY", 5, 7, iron_condor_legs)
# await run_bot_with_params("SPY", 5, 7, king_condor_legs)
