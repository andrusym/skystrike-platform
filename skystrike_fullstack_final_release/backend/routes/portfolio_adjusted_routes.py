from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
import os, json

router = APIRouter()

PROFILE_PATH = os.path.expanduser("~/skystrike-data/portfolio_profiles.json")
METRICS_PATH = os.path.expanduser("~/skystrike-data/bot_metrics.json")

def load_json(path, fallback):
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(fallback, f, indent=2)
    with open(path, "r") as f:
        return json.load(f)

def scale_by_metrics(base_alloc, metrics, capital):
    factor = capital / 10000
    adjusted = {}

    for bot, base in base_alloc.items():
        win_rate = metrics.get(bot, {}).get("win_rate", 0.5)
        streak = sum(metrics.get(bot, {}).get("last_10", [])[-3:])
        pnl = metrics.get(bot, {}).get("pnl", 0)

        size = base * factor

        if win_rate > 0.7 and pnl > 0 and streak >= 2:
            size *= 1.5
        elif win_rate < 0.5 and streak <= -2:
            size *= 0.5

        adjusted[bot] = max(0, round(size))

    return adjusted

@router.get("/api/portfolio/adjusted-recommendation")
def adjusted_recommendation(
    profile: str = Query("balanced"),
    capital: int = Query(10000)
):
    profiles = load_json(PROFILE_PATH, {})
    metrics = load_json(METRICS_PATH, {})

    base = profiles.get(profile.lower())
    if not base:
        return JSONResponse(status_code=400, content={"error": "Invalid profile"})

    scaled = scale_by_metrics(base, metrics, capital)

    return {
        "profile": profile,
        "capital": capital,
        "contracts": scaled,
        "metrics": metrics
    }
