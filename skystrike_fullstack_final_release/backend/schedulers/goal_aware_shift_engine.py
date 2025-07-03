import json

def run_goal_aware_shift(goal="growth"):
    profile_map = {
        "growth": {
            "ironcondor": 3,
            "momentumbot": 2
        },
        "income": {
            "wheel": 2,
            "csp": 2,
            "spread": 2
        },
        "preserve": {
            "ironcondor": 1,
            "pairstrader": 1
        },
        "balanced": {
            "ironcondor": 2,
            "spread": 1,
            "momentumbot": 1
        }
    }

    raw = profile_map.get(goal.lower(), {})
    wrapped = {
        bot: {
            "contracts": contracts,
            "ticker": "SPY",       # Default fallback ticker
            "active": True
        }
        for bot, contracts in raw.items()
    }

    with open("ml/goal_recommendation.json", "w") as f:
        json.dump(wrapped, f, indent=2)

    print(f"? Goal-aware recommendation saved for goal: {goal} with {len(wrapped)} bots")
    return wrapped

def shift_portfolio_by_goal(bot_status: dict, goal: str) -> dict:
    """
    Adjusts contract sizing or allocations based on the user’s selected goal.
    'growth' = more aggressive bots weighted higher
    'income' = income-focused bots like CSP, Wheel, Condors weighted
    'preservation' = less risk, fewer contracts

    Returns a dict of adjusted bot contracts.
    """
    print(f"🎯 Shifting portfolio for goal: {goal}")
    weights = {}

    if goal == "growth":
        weights = {bot: 2 for bot in bot_status if bot_status[bot] == "active"}
    elif goal == "income":
        income_bots = {"ironcondor", "kingcondor", "wheel", "csp"}
        weights = {
            bot: 2 if bot in income_bots and bot_status[bot] == "active" else 1
            for bot in bot_status
        }
    elif goal == "preservation":
        weights = {bot: 1 for bot in bot_status if bot_status[bot] == "active"}

    adjusted = {}
    for bot, status in bot_status.items():
        if status == "active":
            adjusted[bot] = weights.get(bot, 1)
        elif status == "cooldown":
            adjusted[bot] = 0
        else:  # degraded or disabled
            adjusted[bot] = 0

    print("📊 Adjusted allocation:", adjusted)
    return adjusted

def shift_portfolio_by_goal(bot_status: dict, goal: str) -> dict:
    """
    Adjusts contract sizing or allocations based on the user’s selected goal.
    'growth' = more aggressive bots weighted higher
    'income' = income-focused bots like CSP, Wheel, Condors weighted
    'preservation' = less risk, fewer contracts

    Returns a dict of adjusted bot contracts.
    """
    print(f"🎯 Shifting portfolio for goal: {goal}")
    weights = {}

    if goal == "growth":
        weights = {bot: 2 for bot in bot_status if bot_status[bot] == "active"}
    elif goal == "income":
        income_bots = {"ironcondor", "kingcondor", "wheel", "csp"}
        weights = {
            bot: 2 if bot in income_bots and bot_status[bot] == "active" else 1
            for bot in bot_status
        }
    elif goal == "preservation":
        weights = {bot: 1 for bot in bot_status if bot_status[bot] == "active"}

    adjusted = {}
    for bot, status in bot_status.items():
        if status == "active":
            adjusted[bot] = weights.get(bot, 1)
        elif status == "cooldown":
            adjusted[bot] = 0
        else:  # degraded or disabled
            adjusted[bot] = 0

    print("📊 Adjusted allocation:", adjusted)
    return adjusted
