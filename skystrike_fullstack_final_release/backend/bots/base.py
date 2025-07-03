from backend.services.tradier_client import TradierClient
import os
import logging
from datetime import date, timedelta
from dateutil import parser
from typing import List, Dict, Any, Optional

import requests

logger = logging.getLogger(__name__)

SANDBOX_BASE = "https://sandbox.tradier.com/v1"
LIVE_BASE    = "https://api.tradier.com/v1"

class TradierClient:
    def __init__(
        self,
        token: Optional[str]      = None,
        account_id: Optional[str] = None,
        sandbox: bool             = True,
    ):
        if token:
            self.token = token
        else:
            self.token = os.getenv("TRADIER_PAPER_ACCESS_TOKEN") if sandbox else os.getenv("TRADIER_LIVE_ACCESS_TOKEN")
        if not self.token:
            raise ValueError("Must set TRADIER_PAPER_ACCESS_TOKEN or TRADIER_LIVE_ACCESS_TOKEN")

        if account_id:
            self.account_id = account_id
        else:
            self.account_id = os.getenv("TRADIER_PAPER_ACCOUNT_ID") if sandbox else os.getenv("TRADIER_LIVE_ACCOUNT_ID")
        if not self.account_id:
            raise ValueError("Must set TRADIER_PAPER_ACCOUNT_ID or TRADIER_LIVE_ACCOUNT_ID")

        self.base    = SANDBOX_BASE if sandbox else LIVE_BASE
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.token}",
            "Accept":        "application/json",
        })

    def _get(self, path: str, params: dict = None) -> dict:
        url = f"{self.base}{path}"
        r = self.session.get(url, params=params or {})
        r.raise_for_status()
        return r.json()

    def _post(self, path: str, data: dict) -> dict:
        url = f"{self.base}{path}"
        print(f"[POST] URL: {url}")
        print(f"[POST] DATA: {data}")
        r = self.session.post(
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

    def _send_order(self, payload: dict) -> dict:
        """
        Used by bots to submit raw Tradier order payloads.
        """
        url = f"{self.base}/accounts/{self.account_id}/orders"
        print(f"[POST] URL: {url}")
        print(f"[POST] PAYLOAD: {payload}")
        r = self.session.post(
            url,
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        print(f"[POST] STATUS: {r.status_code}")
        try:
            print(f"[POST] RESPONSE: {r.json()}")
        except Exception:
            print(f"[POST] TEXT RESPONSE: {r.text}")
        r.raise_for_status()
        return r.json()

    def get_expirations(self, symbol: str) -> List[str]:
        data = self._get("/markets/options/expirations", {"symbol": symbol})
        return data.get("expirations", {}).get("date", [])

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        data = self._get("/markets/quotes", {"symbols": symbol})
        return data.get("quotes", {}).get("quote", {})

    def format_option(self, ticker: str, expiration: str, right: str, strike: float) -> str:
        s = f"{int(strike * 1000):08d}"
        return f"{ticker}{expiration}{right}{s}"

    def submit_multileg(self, symbol: str, legs: List[Dict[str, Any]], price: float = 1.0) -> dict:
        payload = {
            "class":    "multileg",     # ? FIXED
            "type":     "limit",        # ? FIXED: use 'limit' for spreads
            "symbol":   symbol,
            "duration": "day",
            "price":    str(price),
        }
        for i, leg in enumerate(legs):
            payload[f"option_symbol[{i}]"] = leg["option_symbol"]
            payload[f"side[{i}]"]          = leg["side"]
            payload[f"quantity[{i}]"]      = str(leg["quantity"])
        return self._post(f"/accounts/{self.account_id}/orders", payload)

    def submit_equity(self, symbol: str, side: str, qty: int, price: float = None) -> dict:
        payload = {
            "class":    "equity",
            "symbol":   symbol,
            "side":     side,
            "quantity": str(qty),
            "duration": "day",
            "type":     "market" if price is None else "limit",
        }
        if price is not None:
            payload["price"] = str(price)
        return self._post(f"/accounts/{self.account_id}/orders", payload)
