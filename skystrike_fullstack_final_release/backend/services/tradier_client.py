import os
import json
import logging
import httpx
from datetime import datetime
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

# Load .env from project root
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))

SANDBOX_BASE = "https://sandbox.tradier.com/v1"
LIVE_BASE    = "https://api.tradier.com/v1"

# module-level logger
logger = logging.getLogger(__name__)

class TradierClient:
    def __init__(self, mode: str = "paper"):
        self.base = SANDBOX_BASE if mode == "paper" else LIVE_BASE
        self.token = (
            os.getenv("TRADIER_PAPER_ACCESS_TOKEN")
            if mode == "paper"
            else os.getenv("TRADIER_LIVE_ACCESS_TOKEN")
        )
        self.account_id = (
            os.getenv("TRADIER_PAPER_ACCOUNT_ID")
            if mode == "paper"
            else os.getenv("TRADIER_LIVE_ACCOUNT_ID")
        )
        if not self.token or not self.account_id:
            raise ValueError("Missing Tradier token or account ID")

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept":        "application/json",
            "Content-Type":  "application/x-www-form-urlencoded",
        }

    async def _get(self, path: str, params: dict = None) -> dict:
        url = f"{self.base}{path}"
        async with httpx.AsyncClient() as client:
            r = await client.get(url, headers=self.headers, params=params or {})
            r.raise_for_status()
            return r.json()

    async def _post(self, path: str, data: dict) -> dict:
        # only emit payload when debug is enabled
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("Payload Debug:\n%s", json.dumps(data, indent=2))

        url = f"{self.base}{path.format(account_id=self.account_id)}"
        async with httpx.AsyncClient() as client:
            r = await client.post(url, headers=self.headers, data=data)
            r.raise_for_status()
            return r.json()

    async def get_expirations(self, symbol: str) -> List[str]:
        data = await self._get("/markets/options/expirations", {"symbol": symbol})
        return data.get("expirations", {}).get("date", [])

    async def get_option_chain(self, symbol: str, expiration: str) -> Dict[str, Any]:
        data = await self._get(
            "/markets/options/chains",
            {"symbol": symbol, "expiration": expiration},
        )
        opts = data.get("options", {})
        return {"options": opts.get("option", [])} if isinstance(opts, dict) else {"options": []}

    async def get_quote(self, symbol: str) -> Dict[str, Any]:
        data = await self._get("/markets/quotes", {"symbols": symbol})
        qs = data.get("quotes", {}).get("quote", [])
        return qs[0] if isinstance(qs, list) else qs

    def format_option(self, ticker: str, expiration: str, right: str, strike: float) -> str:
        try:
            exp_date = datetime.strptime(expiration, "%Y-%m-%d")
        except ValueError:
            exp_date = datetime.strptime(expiration, "%Y%m%d")
        date_fmt   = exp_date.strftime("%y%m%d")
        strike_fmt = f"{int(strike * 1000):08d}"
        return f"{ticker.upper()}{date_fmt}{right.upper()}{strike_fmt}"

    async def submit_multileg(
        self,
        symbol: str,
        legs: List[Dict[str, Any]],
        price: Optional[float] = None,
        order_type: str = "credit"  # one of: market, debit, credit, even
    ) -> dict:
        payload: Dict[str, str] = {
            "class":    "multileg",
            "type":     order_type,
            "symbol":   symbol,
            "duration": "day",
        }
        if order_type in ("debit", "credit", "even") and price is not None:
            payload["price"] = f"{price:.2f}"

        for i, leg in enumerate(legs):
            payload[f"option_symbol[{i}]"] = leg["option_symbol"]
            payload[f"side[{i}]"]          = leg["side"]
            payload[f"quantity[{i}]"]      = str(leg["quantity"])

        return await self._post("/accounts/{account_id}/orders", payload)

    async def submit_equity(
        self,
        symbol: str,
        side: str,
        qty: int,
        price: Optional[float] = None
    ) -> dict:
        payload = {
            "class":    "equity",
            "symbol":   symbol,
            "side":     side,
            "quantity": str(qty),
            "duration": "day",
            "type":     "limit" if price is not None else "market",
        }
        if price is not None:
            payload["price"] = f"{price:.2f}"
        return await self._post("/accounts/{account_id}/orders", payload)

    async def submit_option_order(
        self,
        option_symbol: str,
        side: str,
        quantity: int,
        price: Optional[float] = None
    ) -> dict:
        payload = {
            "class":         "option",
            "symbol":        option_symbol[:-15],
            "option_symbol": option_symbol,
            "side":          side,
            "quantity":      str(quantity),
            "duration":      "day",
            "type":          "limit" if price is not None else "market",
        }
        if price is not None:
            payload["price"] = f"{price:.2f}"
        return await self._post("/accounts/{account_id}/orders", payload)
