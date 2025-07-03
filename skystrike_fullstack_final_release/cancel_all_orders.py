import requests

TRADIER_API_URL = "https://sandbox.tradier.com/v1"
ACCESS_TOKEN = "RlLmD2V8FKCJAcuj9KQoKpU5TeKt"
ACCOUNT_ID = "VA70062258"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Accept": "application/json"
}

# Step 1: Get open orders
def get_open_orders():
    url = f"{TRADIER_API_URL}/accounts/{ACCOUNT_ID}/orders"
    response = requests.get(url, headers=headers)
    orders = response.json().get("orders", {}).get("order", [])
    if isinstance(orders, dict):
        return [orders]
    return orders

# Step 2: Cancel each open order
def cancel_order(order_id):
    url = f"{TRADIER_API_URL}/accounts/{ACCOUNT_ID}/orders/{order_id}/cancel"
    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        print(f"✅ Cancelled order {order_id}")
    else:
        print(f"❌ Failed to cancel {order_id}: {response.text}")

# Main runner
if __name__ == "__main__":
    open_orders = get_open_orders()
    if not open_orders:
        print("No open orders to cancel.")
    else:
        for order in open_orders:
            if order.get("status") == "open":
                cancel_order(order["id"])
