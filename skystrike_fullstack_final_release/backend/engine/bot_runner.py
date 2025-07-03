import json
import uuid
from datetime import datetime
from core.users import load_users
from core.tradier import submit_order  # placeholder import for execution

ALLOCATION_FILE = "data/strategy_allocation.json"
TRADE_LOG = "data/trade_log.json"

def place_order_for_bot(bot_name, quantity, user_profile, ticker="SPY"):
    symbol = ticker
    order_type = "iron_condor" if "Condor" in bot_name else "spread"
    order_id = str(uuid.uuid4())
    log_entry = {
        "id": order_id,
        "timestamp": datetime.utcnow().isoformat(),
        "strategy": bot_name,
        "symbol": symbol,
        "quantity": quantity,
        "order_type": order_type,
        "user": user_profile.get("username")
    }

    token = user_profile.get("tradier_token")
    mode = user_profile.get("tradier_mode", "paper")
    response = submit_order(symbol, quantity, token, mode, bot_name)
    log_entry["broker_status"] = response.get("status", "submitted")

    try:
        with open(TRADE_LOG, "r+") as f:
            trades = json.load(f)
            trades.append(log_entry)
            f.seek(0)
            json.dump(trades, f, indent=2)
    except FileNotFoundError:
        with open(TRADE_LOG, "w") as f:
            json.dump([log_entry], f, indent=2)

    return log_entry

def run_all_bots():
    users = load_users()
    with open(ALLOCATION_FILE, "r") as f:
        allocation = json.load(f)

    for bot, details in allocation.items():
        for username, profile in users.items():
            profile["username"] = username
            for ticker, config in details["tickers"].items():
                qty = config.get("contracts", 1)
                place_order_for_bot(bot, qty, profile, ticker)

if __name__ == "__main__":
    run_all_bots()
