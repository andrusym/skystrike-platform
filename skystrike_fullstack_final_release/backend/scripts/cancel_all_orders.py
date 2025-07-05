# backend/scripts/cancel_all_orders.py

import os
import requests
from dotenv import load_dotenv
from pathlib import Path

# Force load .env from project root (one level up)
load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")

# Use sandbox API by default
TRADIER_API_URL = os.getenv("TRADIER_API_URL", "https://sandbox.tradier.com/v1")
ACCESS_TOKEN = os.getenv("TRADIER_SANDBOX_ACCESS_TOKEN")
ACCOUNT_ID = os.getenv("TRADIER_SANDBOX_ACCOUNT_ID")

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Accept": "application/json"
}

def get_open_orders():
    url = f"{TRADIER_API_URL}/accounts/{ACCOUNT_ID}/orders"
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        print(f"? Failed to fetch orders: {resp.status_code} {resp.text}")
        return []

    orders = resp.json().get("orders", {}).get("order", [])
    return [orders] if isinstance(orders, dict) else orders

def cancel_order(order_id):
    url = f"{TRADIER_API_URL}/accounts/{ACCOUNT_ID}/orders/{order_id}"
    resp = requests.delete(url, headers=headers)
    if resp.status_code == 200:
        print(f"? Cancelled order {order_id}")
    else:
        print(f"?? Failed to cancel {order_id}: {resp.status_code} {resp.text}")

def is_cancelable(order):
    return order.get("status") in ["open", "pending", "queued"]

if __name__ == "__main__":
    orders = get_open_orders()
    if not orders:
        print("?? No open orders found.")
    else:
        print(f"?? Found {len(orders)} order(s). Attempting cancel...")
        for order in orders:
            if is_cancelable(order):
                cancel_order(order["id"])
            else:
                print(f"?? Skipping order {order['id']} (status: {order['status']}, class: {order.get('class')})")
