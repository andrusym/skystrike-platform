import json
core.bot_runner import place_order_for_bot
core.users import load_users
core.lifecycle_engine import is_in_cooldown

CONFIG_PATH = "data/bot_config.json"

def run_bots():
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
    users = load_users()

    for bot, settings in config.items():
        if settings.get("status") != "active":
            continue
        if is_in_cooldown(bot):
            continue
        for username, profile in users.items():
            profile["username"] = username
            qty = settings.get("contracts", 1)
            place_order_for_bot(bot, qty, profile)

if __name__ == "__main__":
    run_bots()
