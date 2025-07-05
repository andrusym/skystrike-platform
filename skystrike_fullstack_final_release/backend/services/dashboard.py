# backend/services/dashboard.py

import os
import json
import datetime

from backend.services.tradier_client import TradierClient
from backend.engine.portfolio_metrics import compute_win_rate, compute_strategy_distribution
from backend.engine.ml_engine import get_ml_status
from backend.engine.fallback_engine import get_fallback_status
from backend.portfolio.final_recommendation import get_final_recommendation

# Paths
BOT_CONFIG_PATH = "config/bot_config.json"
ML_SCORES_PATH = "ml/ml_scores.json"
COOLDOWN_PATH = "config/cooldowns.json"

# Instantiate the broker client
_client = TradierClient()


def get_dashboard_metrics() -> dict:
    """Gather and return all high-level metrics for the SkyStrike dashboard."""
    try:
        balances = _client.get_balances()
    except Exception as e:
        balances = {}
        print(f"?? Error fetching balances: {e}")

    try:
        orders = _client.get_open_orders()
    except Exception as e:
        orders = []
        print(f"?? Error fetching open orders: {e}")

    try:
        positions = _client.get_open_positions()
    except Exception as e:
        positions = []
        print(f"?? Error fetching open positions: {e}")

    try:
        win_rate = compute_win_rate()
    except Exception as e:
        win_rate = None
        print(f"?? Error computing win rate: {e}")

    try:
        strat_dist = compute_strategy_distribution()
    except Exception as e:
        strat_dist = {}
        print(f"?? Error computing strategy distribution: {e}")

    try:
        ml_status = get_ml_status()
    except Exception as e:
        ml_status = {"error": str(e)}

    try:
        fallback = get_fallback_status()
    except Exception as e:
        fallback = False

    try:
        recommendation = get_final_recommendation()
    except Exception as e:
        recommendation = {"error": str(e)}

    return {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "net_liquidation": balances.get("total_equity", 0.0),
        "buying_power": balances.get("buying_power", 0.0),
        "open_positions": positions,
        "open_orders": orders,
        "win_rate": win_rate,
        "strategy_distribution": strat_dist,
        "ml_status": ml_status,
        "fallback_active": fallback,
        "final_recommendation": recommendation
    }


def get_strategy_status() -> dict:
    """
    Load bot config, ML scores, and cooldowns into a unified bot status structure.
    Used by dashboard or admin panel to show toggles and metadata.
    """
    try:
        with open(BOT_CONFIG_PATH, "r") as f:
            bot_config = json.load(f)
    except Exception as e:
        return {"error": f"Failed to load bot_config.json: {str(e)}"}

    try:
        with open(ML_SCORES_PATH, "r") as f:
            ml_scores = json.load(f)
    except:
        ml_scores = {}

    try:
        with open(COOLDOWN_PATH, "r") as f:
            cooldowns = json.load(f)
    except:
        cooldowns = {}

    enriched = {}
    for bot, cfg in bot_config.items():
        enriched[bot] = {
            "status": cfg.get("status", "unknown"),
            "active": cfg.get("active", False),
            "contracts": cfg.get("contracts", 0),
            "confidence": ml_scores.get(bot, {}).get("confidence"),
            "cooldown_expires": cooldowns.get(bot)
        }

    return {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "strategies": enriched
    }
