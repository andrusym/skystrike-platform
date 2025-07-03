from fastapi import APIRouter
import json

router = APIRouter(prefix="/api/portfolio")

@router.get("/recommendation")
def get_portfolio_recommendation():
    with open("data/strategy_allocation.json") as f:
        base_allocation = json.load(f)
    with open("data/portfolio_profiles.json") as f:
        profiles = json.load(f)
    with open("data/users.json") as f:
        users = json.load(f)

    # Assume single user for now
    username, user_data = next(iter(users.items()))
    goal = user_data.get("goal", "conservative")
    scale = profiles.get(goal, {}).get("scale", 1.0)

    scaled = {}
    for strategy, cfg in base_allocation.items():
        scaled[strategy] = {
            "style": cfg["style"],
            "execution_window": cfg["execution_window"],
            "tickers": {
                ticker: {
                    "capital": round(data["capital"] * scale),
                    "contracts": int(data["contracts"] * scale)
                }
                for ticker, data in cfg["tickers"].items()
            }
        }

    return {"profile": goal, "scaled_allocation": scaled}
