from backend.services.tradier_client import TradierClient

def main():
    client = TradierClient()

    order_spec = {
        "endpoint": f"/accounts/{client.account_id}/orders",
        "payload": {
            "class": "equity",
            "symbol": "AAPL",
            "side": "buy",
            "quantity": "1",
            "type": "market",
            "duration": "day"
        }
    }

    try:
        response = client.submit_order(order_spec)
        print("Order response:", response)
    except Exception as e:
        print("Error submitting order:", e)

if __name__ == "__main__":
    main()
