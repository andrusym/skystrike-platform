#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# 1) Write the updated Tradier service
cat > backend/services/tradier_api.py << 'EOF'
$(sed -n '1,200p' << 'PYCODE'
import os
import requests
from datetime import date, timedelta

TRADIER_BASE_URL = "https://api.tradier.com/v1"
MODE               = os.getenv("TRADIER_MODE", "paper").upper()
TRADIER_TOKEN      = os.getenv(f"TRADIER_${MODE}_ACCESS_TOKEN")
TRADIER_ACCOUNT_ID = os.getenv(f"TRADIER_${MODE}_ACCOUNT_ID")

def get_quote(symbol: str) -> dict:
    headers = {
        "Authorization": f"Bearer {TRADIER_TOKEN}",
        "Accept":        "application/json",
    }
    resp = requests.get(
        f"{TRADIER_BASE_URL}/markets/quotes",
        params={"symbols": symbol},
        headers=headers
    )
    resp.raise_for_status()
    return resp.json()["quotes"]["quote"]

def place_iron_condor(ticker: str, contracts: int, dte: int) -> dict:
    exp_date = date.today() + timedelta(days=dte)
    exp_str  = exp_date.strftime("%y%m%d")

    quote      = get_quote(ticker)
    last_price = float(quote["last"])

    width = 5.0
    atm   = round(last_price / width) * width
    strikes = {
        "short_call": atm + width,
        "long_call":  atm + 2 * width,
        "short_put":  atm - width,
        "long_put":   atm - 2 * width,
    }

    def occ_symbol(strike: float, right: str) -> str:
        s = f"{int(strike * 1000):08d}"
        return f"{ticker}{exp_str}{right}{s}"

    data = {
      "class":    "multileg",
      "symbol":   ticker,
      "duration": "day",
      "option_symbol[0]": occ_symbol(strikes["short_call"], "C"),
      "side[0]":          "sell_to_open",
      "quantity[0]":      contracts,
      "option_symbol[1]": occ_symbol(strikes["long_call"], "C"),
      "side[1]":          "buy_to_open",
      "quantity[1]":      contracts,
      "option_symbol[2]": occ_symbol(strikes["short_put"], "P"),
      "side[2]":          "sell_to_open",
      "quantity[2]":      contracts,
      "option_symbol[3]": occ_symbol(strikes["long_put"], "P"),
      "side[3]":          "buy_to_open",
      "quantity[3]":      contracts,
    }

    headers = {
      "Authorization":   f"Bearer {TRADIER_TOKEN}",
      "Accept":          "application/json",
      "Content-Type":    "application/x-www-form-urlencoded",
    }
    resp = requests.post(
      f"{TRADIER_BASE_URL}/accounts/{TRADIER_ACCOUNT_ID}/orders",
      headers=headers,
      data=data
    )
    resp.raise_for_status()
    return resp.json()
PYCODE
)
EOF

# 2) Write the updated order route
cat > backend/routes/order_routes.py << 'EOF'
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
services.tradier_api import place_iron_condor
auth import get_current_user, User

router = APIRouter(prefix="/orders", tags=["orders"])

class IronCondorPayload(BaseModel):
    strategy:  str
    ticker:    str
    contracts: int
    dte:       int

@router.post("/place")
async def place_order(
    payload: IronCondorPayload,
    current_user: User = Depends(get_current_user)
):
    if payload.strategy != "iron_condor":
        raise HTTPException(status_code=400, detail="Unsupported strategy")
    try:
        broker_response = place_iron_condor(
            payload.ticker,
            payload.contracts,
            payload.dte
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))
    return {
        "status":          "order submitted",
        "strategy":        payload.strategy,
        "ticker":          payload.ticker,
        "contracts":       payload.contracts,
        "broker_response": broker_response
    }
EOF

# 3) Restart the app
echo "? Patch applied. Restarting Uvicorn..."
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
