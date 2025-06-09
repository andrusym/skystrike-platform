
import datetime
import random

def check_exit_conditions(trade):
    """
    Evaluates whether a trade should be closed based on profit, time decay, or risk thresholds.
    """
    if trade["status"] != "OPEN":
        return False

    # Simulate profit check
    current_price = simulate_current_price(trade["entry_price"])
    profit = current_price - trade["entry_price"]

    # Time decay / expiration proximity
    entry_time = datetime.datetime.fromisoformat(trade["entry_time"])
    days_open = (datetime.datetime.now() - entry_time).days

    # Guardrails
    max_holding_days = 5
    profit_threshold = 0.5  # in dollars
    loss_cutoff = -1.0      # in dollars

    if profit >= profit_threshold:
        trade["reason"] = "Target profit hit"
        return True
    elif profit <= loss_cutoff:
        trade["reason"] = "Max loss threshold hit"
        return True
    elif days_open >= max_holding_days:
        trade["reason"] = "Max days open hit"
        return True
    return False

def simulate_current_price(entry_price):
    change = random.uniform(-1.25, 1.25)
    return round(entry_price + change, 2)
