# backend/admin/admin_user_manager.py

import asyncio
from backend.services.tradier_api import get_open_orders

def get_user_stats():
    """
    Grabs queued orders count from Tradier.
    """
    data = asyncio.run(get_open_orders())
    orders = data.get("orders", {}).get("order", [])
    count = len(orders) if isinstance(orders, list) else (1 if orders else 0)
    return {
        "queued_orders": count,
        "active_sessions": 0  # implement your session counting as needed
    }
