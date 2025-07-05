# backend/services/order_submission.py

import os
import time
import requests
from typing import Dict, Any
from backend.config import settings

TRADIER_BASE = (
    "https://api.tradier.com/v1" if settings.TRADE_MODE == "live"
    else "https://sandbox.tradier.com/v1"
)

HEADERS = {
    "Authorization": f"Bearer {settings.TRADIER_API_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded",
}


def submit_multileg_order(order_payload: Dict[str, Any]) -> Dict[str, Any]:
    """Submit a multi-leg options order to Tradier."""
    url = f"{TRADIER_BASE}/accounts/{settings.TRADIER_ACCOUNT_ID}/orders"
    response = requests.post(url, data=order_payload, headers=HEADERS)
    try:
        data = response.json()
    except Exception:
        data = {"error": "non-JSON response", "status_code": response.status_code}

    return {
        "status_code": response.status_code,
        "response": data,
        "submitted_payload": order_payload,
    }


def submit_option_order(order_payload: Dict[str, Any]) -> Dict[str, Any]:
    """Submit a single-leg options order (basic wrapper around Tradier API)."""
    url = f"{TRADIER_BASE}/accounts/{settings.TRADIER_ACCOUNT_ID}/orders"
    response = requests.post(url, data=order_payload, headers=HEADERS)
    try:
        data = response.json()
    except Exception:
        data = {"error": "non-JSON response", "status_code": response.status_code}

    return {
        "status_code": response.status_code,
        "response": data,
        "submitted_payload": order_payload,
    }


def submit_equity_order(order_payload: Dict[str, Any]) -> Dict[str, Any]:
    """Submit an equity order (used by CSP, Wheel, or ETF logic)."""
    url = f"{TRADIER_BASE}/accounts/{settings.TRADIER_ACCOUNT_ID}/orders"
    response = requests.post(url, data=order_payload, headers=HEADERS)
    try:
        data = response.json()
    except Exception:
        data = {"error": "non-JSON response", "status_code": response.status_code}

    return {
        "status_code": response.status_code,
        "response": data,
        "submitted_payload": order_payload,
    }
