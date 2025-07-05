from backend.services.tradier_client import TradierClient
from datetime import date, timedelta

async def get_valid_expiration(ticker: str, target_dte: int = 1, mode: str = "paper") -> str:
    """
    Returns the safest Tradier-supported expiration date:
    - Prefers exact match to today + DTE
    - Otherwise picks first expiration after that date
    """
    client = TradierClient(mode=mode)
    expirations = await client.get_expirations(ticker)
    target_date = date.today() + timedelta(days=target_dte)

    if not expirations:
        raise ValueError(f"No expirations found for {ticker}")

    valid_dates = sorted([date.fromisoformat(e) for e in expirations])
    target_str = target_date.strftime("%Y-%m-%d")

    # 1. Try exact match
    if target_str in expirations:
        return target_str

    # 2. Find the next available expiration after target
    for exp_date in valid_dates:
        if exp_date > target_date:
            return exp_date.strftime("%Y-%m-%d")

    # 3. Fallback to last known expiration (should never hit this)
    return valid_dates[-1].strftime("%Y-%m-%d")