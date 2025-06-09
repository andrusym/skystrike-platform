
import uuid
import datetime
import random
import logging

def execute_trade(ticker, setup, capital, trade_id=None, mode="paper"):
    if not trade_id:
        trade_id = str(uuid.uuid4())

    trade = {
        "id": trade_id,
        "ticker": ticker,
        "strategy": setup.get("type"),
        "legs": setup.get("legs"),
        "entry_time": setup.get("entry_time", datetime.datetime.now().isoformat()),
        "status": "OPEN",
        "capital": capital,
        "mode": mode,
        "entry_price": simulate_entry_price(setup),
        "target_exit": calculate_target_exit(setup, capital),
    }

    logging.info(f"[{mode.upper()}] Trade Executed: {trade}")
    return trade

def close_trade(trade):
    trade["exit_time"] = datetime.datetime.now().isoformat()
    trade["status"] = "CLOSED"
    trade["exit_price"] = simulate_exit_price(trade["entry_price"])
    trade["pnl"] = trade["exit_price"] - trade["entry_price"]
    logging.info(f"Trade Closed: {trade['id']} | PnL: {trade['pnl']}")
    return trade

def simulate_entry_price(setup):
    legs = setup.get("legs", {})
    base_price = sum(random.uniform(0.5, 2.0) for _ in legs)
    return round(base_price, 2)

def simulate_exit_price(entry_price):
    change = random.uniform(-0.75, 0.75)
    return round(entry_price + change, 2)

def calculate_target_exit(setup, capital):
    base_target = capital * 0.01
    risk_profile = setup.get("type", "iron_condor")
    multiplier = {
        "iron_condor": 1.0,
        "iron_fly": 1.2,
        "calendar_spread": 0.9
    }.get(risk_profile, 1.0)
    return round(base_target * multiplier, 2)
