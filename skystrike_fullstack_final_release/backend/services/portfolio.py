# backend/services/portfolio.py

from typing import Dict
from backend import bots as bots_pkg

def preview_sizing(*, account_size: float, user) -> Dict[str, Dict]:
    """
    Stub for portfolio sizing. Returns a simple 'equal-contract' recommendation
    for each bot in __all__, based on account_size.
    You can replace this with your real ML-driven logic later.
    """
    BOT_NAMES = getattr(bots_pkg, "__all__", [])
    if not BOT_NAMES:
        return {}
    # Simple example: split account_size equally across bots,
    # assume each contract is priced at $1000 for sizing
    per_bot = account_size / len(BOT_NAMES)
    contracts = max(1, int(per_bot // 1000))

    return {
        bot: {
            "recommendedContracts": contracts,
            "allocatedCapital": round(per_bot, 2),
            "userGoal": getattr(user, "goal", None)
        }
        for bot in BOT_NAMES
    }
