from fastapi import APIRouter
from backend.services.log_reader import load_trade_log

router = APIRouter()

# TEMP: stub for broker order history (until real Tradier integration is added)
def fetch_order_status() -> dict:
    return {
        "orders": [
            {"id": "stub-001", "status": "filled", "symbol": "SPY"},
            {"id": "stub-002", "status": "pending", "symbol": "QQQ"},
        ]
    }

@router.get("/api/orders/history")
def get_order_history():
    trade_log = load_trade_log()
    broker_orders = fetch_order_status().get("orders", [])
    return {"trades": trade_log, "broker_orders": broker_orders}
