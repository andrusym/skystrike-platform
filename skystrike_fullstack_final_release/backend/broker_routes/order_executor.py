def execute_order(order):
    return {
        "status": "executed",
        "details": {
            "symbol": order.get("symbol"),
            "type": order.get("type"),
            "price": order.get("price", 0),
            "timestamp": "2025-06-09T00:00:00Z"
        }
    }