#!/usr/bin/env python3
# coding: utf-8

import json
import random
from datetime import datetime
from backend.engine.plugin_loader import run_hook

ML_SCORES_FILE        = "data/ml_scores.json"
TICKER_CONFIG_FILE    = "config/ticker_config.json"
CONTRACT_LIMITS_FILE  = "config/contract_limits.json"
BOT_CONFIG_FILE       = "config/bot_config.json"

BOT_LIST = [
    "ironcondor", "kingcondor", "wheel", "spread", "csp", "dcabot",
    "scalper", "momentumbot", "trend", "replicator", "breakoutbot",
    "copybot", "gridbot", "straddlebot", "gammafly", "squeezehunter",
    "earningsbot", "calendarbot", "equity_buy", "volharvest",
    "pairstrader", "ratioflybot"
]

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def orchestrate():
    guardrail = run_hook("backend.engine.drawdown_guardrails.check_equity_guardrail")
    if guardrail.get("guardrail_triggered"):
        print("Equity guardrail triggered. No bots will run.")
        return {"status": "blocked", "reason": "portfolio drawdown guardrail"}

    ml_scores     = load_json(ML_SCORES_FILE)
    drawdowns     = run_hook("backend.engine.bot_drawdown_engine.check_bot_drawdowns")
    adaptive      = run_hook("backend.engine.adaptive_sizing_engine.load_adaptive_contracts")
    dte_info      = run_hook("backend.engine.dynamic_dte_selector.select_dte")
    ticker_config = load_json(TICKER_CONFIG_FILE)
    contract_limits = load_json(CONTRACT_LIMITS_FILE)
    bot_config    = load_json(BOT_CONFIG_FILE)

    summary = {}

    for bot in BOT_LIST:
        confidence    = ml_scores.get(bot, {}).get("confidence", 0)
        drawdown_flag = drawdowns.get(bot, {}).get("cooldown_triggered", False)
        contracts     = adaptive.get(bot, {}).get("contracts", 0)
        tickers       = ticker_config.get(bot, [])
        override      = bot_config.get(bot, {}).get("override", "none")

        if not tickers:
            summary[bot] = {"skipped": True, "reason": "no tickers defined"}
            continue

        ticker = random.choice(tickers)
        max_allowed = contract_limits.get(bot, {}).get(ticker, 100)

        if override == "disabled":
            summary[bot] = {"skipped": True, "reason": "override: disabled"}
            continue
        if override == "cooldown":
            summary[bot] = {"skipped": True, "reason": "override: cooldown"}
            continue
        if override == "active":
            drawdown_flag = False  # Force active

        if drawdown_flag or contracts == 0 or confidence < 0.5:
            summary[bot] = {"skipped": True, "reason": "low confidence or cooldown"}
            continue

        contracts = min(contracts, max_allowed)

        try:
            result = run_hook(
                "backend.services.submit_order.run_bot_with_params",
                bot=bot, ticker=ticker, contracts=contracts, dte=dte_info.get("dte")
            )
            summary[bot] = {
                "skipped": False,
                "ticker": ticker,
                "contracts": contracts,
                "result": result
            }
        except Exception as e:
            summary[bot] = {
                "skipped": False,
                "ticker": ticker,
                "contracts": contracts,
                "error": str(e)
            }

    with open("data/orchestration_log.json", "a", encoding="utf-8") as log:
        log.write(json.dumps({
            "timestamp": datetime.utcnow().isoformat(),
            "summary": summary
        }) + "\n")

    return summary
