import json
import uuid
from datetime import datetime

from backend.utils.users import load_users
from backend.services.tradier_client import TradierClient

ALLOCATION_FILE = "data/strategy_allocation.json"
TRADE_LOG       = "data/trade_log.json"

# Instantiate a single TradierClient for all orders
_tradier_client = TradierClient()

def place_order_for_bot(
    bot_name: str,
    quantity: int,
    user_profile: dict,
    ticker: str = "SPY"
) -> dict:
    symbol = ticker
    order_type = "iron_condor" if "Condor" in bot_name else "spread"
    order_id = str(uuid.uuid4())

    log_entry = {
        "id":        order_id,
        "timestamp": datetime.utcnow().isoformat(),
        "strategy":  bot_name,
        "symbol":    symbol,
        "quantity":  quantity,
        "order_type": order_type,
        "user":       user_profile.get("username"),
    }

    account_id = user_profile.get("tradier_account_id")
    mode       = user_profile.get("tradier_mode", "paper")
    response   = _tradier_client.place_order(
        account_id=account_id,
        payload={
            "symbol":   symbol,
            "quantity": quantity,
            "mode":     mode,
            "strategy": bot_name,
        }
    )
    log_entry["broker_status"] = response.get("status", "submitted")

    try:
        with open(TRADE_LOG, "r+", encoding="utf-8") as f:
            trades = json.load(f)
            trades.append(log_entry)
            f.seek(0)
            json.dump(trades, f, indent=2)
            f.truncate()
    except FileNotFoundError:
        with open(TRADE_LOG, "w", encoding="utf-8") as f:
            json.dump([log_entry], f, indent=2)

    return log_entry

def run_all_bots() -> None:
    users = load_users()
    with open(ALLOCATION_FILE, "r", encoding="utf-8") as f:
        allocation = json.load(f)

    for bot_name, details in allocation.items():
        for username, profile in users.items():
            profile["username"] = username
            for ticker, config in details.get("tickers", {}).items():
                qty = int(config.get("contracts", 1))
                place_order_for_bot(bot_name, qty, profile, ticker)

if __name__ == "__main__":
    run_all_bots()
