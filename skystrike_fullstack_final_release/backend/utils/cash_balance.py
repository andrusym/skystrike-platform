import json
from datetime import datetime
import os

CASH_FILE = os.path.join("backend", "data", "cash_balance.json")

def get_cash_balance():
    try:
        with open(CASH_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "cash": 0.0,
            "timestamp": datetime.utcnow().isoformat()
        }

def update_cash_balance(amount):
    """Sets a new cash balance and updates timestamp."""
    data = {
        "cash": round(amount, 2),
        "timestamp": datetime.utcnow().isoformat()
    }
    os.makedirs(os.path.dirname(CASH_FILE), exist_ok=True)
    with open(CASH_FILE, "w") as f:
        json.dump(data, f, indent=2)
    return data

def adjust_cash_balance(delta):
    """Adjusts the current balance by a delta value."""
    current = get_cash_balance()
    new_amount = current["cash"] + delta
    return update_cash_balance(new_amount)

if __name__ == "__main__":
    print("Current:", get_cash_balance())
    print("Updated:", update_cash_balance(18000.0))  # Example reset
