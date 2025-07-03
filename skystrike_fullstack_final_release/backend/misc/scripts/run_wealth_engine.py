import json
core.wealth_utils import load_wealth_config, log_wealth_event, should_pause_wealth
core.users import load_users

def run():
    config = load_wealth_config()
    users = load_users()

    for username, profile in users.items():
        if profile.get("tradier_mode") != "paper":
            continue
        cash = 2000  # placeholder
        if should_pause_wealth(cash, config):
            print(f"Skipping wealth buys for {username}: insufficient cash")
            continue

        event = {
            "user": username,
            "etf_buys": {"VOO": 1, "QQQ": 1},
            "timestamp": "2025-06-18T14:00:00Z"
        }
        log_wealth_event(event)
        print(f"Wealth engine executed for {username}")

if __name__ == "__main__":
    run()
