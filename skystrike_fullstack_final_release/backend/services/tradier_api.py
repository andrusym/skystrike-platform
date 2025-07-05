import os
import logging
import requests
from datetime import date, timedelta
from typing import Dict, List, Any, Optional
from dateutil import parser

from backend.services.option_lookup import get_tradier_option_symbol

logger = logging.getLogger(__name__)

SANDBOX_BASE = "https://sandbox.tradier.com/v1"
LIVE_BASE    = "https://api.tradier.com/v1"


class TradierClient:
    def __init__(
        self,
        token: Optional[str] = None,
        account_id: Optional[str] = None,
        sandbox: bool = True,
    ):
        # Auth token
        self.token = token or (
            os.getenv("TRADIER_PAPER_ACCESS_TOKEN") if sandbox else os.getenv("TRADIER_LIVE_ACCESS_TOKEN")
        )
        if not self.token:
            raise ValueError("Must set TRADIER_PAPER_ACCESS_TOKEN or TRADIER_LIVE_ACCESS_TOKEN")

        # Account ID
        self.account_id = account_id or (
            os.getenv("TRADIER_PAPER_ACCOUNT_ID") if sandbox else os.getenv("TRADIER_LIVE_ACCOUNT_ID")
        )
        if not self.account_id:
            raise ValueError("Must set TRADIER_PAPER_ACCOUNT_ID or TRADIER_LIVE_ACCOUNT_ID")

        self.base = SANDBOX_BASE if sandbox else LIVE_BASE
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.token}",
            "Accept":        "application/json",
        })

    def _get(self, path: str, params: dict = None) -> dict:
        url = f"{self.base}{path}"
        response = self.session.get(url, params=params or {})
        response.raise_for_status()
        return response.json()

    def _post(self, path: str, data: dict) -> dict:
        url = f"{self.base}{path}"
        logger.debug(f"[POST] URL: {url}")
        logger.debug(f"[POST] DATA: {data}")
        response = self.session.post(
            url,
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        logger.debug(f"[POST] STATUS: {response.status_code}")
        try:
            logger.debug(f"[POST] RESPONSE: {response.json()}")
        except Exception:
            logger.debug(f"[POST] TEXT RESPONSE: {response.text}")
        response.raise_for_status()
        return response.json()

    def _send_order(self, payload: dict) -> dict:
        url = f"{self.base}/accounts/{self.account_id}/orders"
        logger.info(f"Sending order to {url}")
        logger.debug(f"Payload: {payload}")
        response = self.session.post(
            url,
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        try:
            logger.debug(f"Response: {response.json()}")
        except Exception:
            logger.debug(f"Raw text: {response.text}")
        response.raise_for_status()
        return response.json()

    def get_expirations(self, symbol: str) -> List[str]:
        data = self._get("/markets/options/expirations", {"symbol": symbol})
        return data.get("expirations", {}).get("date", [])

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        data = self._get("/markets/quotes", {"symbols": symbol})
        return data.get("quotes", {}).get("quote", {})

    def format_option(self, ticker: str, expiration: str, right: str, strike: float) -> str:
        strike_code = f"{int(strike * 1000):08d}"
        return f"{ticker}{expiration}{right.upper()}{strike_code}"

    def submit_multileg(self, symbol: str, legs: List[Dict[str, Any]], price: float = 1.0) -> dict:
        payload = {
            "class":    "multileg",
            "type":     "limit",
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
