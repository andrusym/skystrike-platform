#!/usr/bin/env python3
import os
import pkgutil
import importlib
import asyncio
import logging
import json
import argparse
from datetime import datetime
from backend.submit_order import run_bot_with_params

# Configure logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=LOG_LEVEL, format="%(message)s")
logger = logging.getLogger(__name__)

# Directories for dynamic discovery
ENGINE_PACKAGES = {
    "filters": "backend.engines.filters",
    "quote_stream": "backend.engines.quote_stream",
    "ml": "backend.ml",
    "goal": "backend.engines.goal",
    "position": "backend.engines.position_tracker",
}

def discover_modules(package_name):
    """
    Dynamically import all modules in a given package.
    """
    pkg = importlib.import_module(package_name)
    modules = []
    for _, module_name, is_pkg in pkgutil.iter_modules(pkg.__path__):
        if not is_pkg:
            full_name = f"{package_name}.{module_name}"
            try:
                module = importlib.import_module(full_name)
                modules.append(module)
            except Exception as e:
                logger.error(f"Failed to import {full_name}: {e}")
    return modules

async def run_pipeline(dry_run: bool = False):
    # 1?? Market-event filter: skip non-trading days
    for filt in discover_modules(ENGINE_PACKAGES["filters"]):
        if hasattr(filt, "is_trading_day"):
            ok = await filt.is_trading_day()
            if not ok:
                logger.info("Market filter: not a trading day. Exiting.")
                return

    # 2?? Fetch quotes
    quotes = {}
    for qmod in discover_modules(ENGINE_PACKAGES["quote_stream"]):
        if hasattr(qmod, "fetch_quotes"):
            try:
                data = await qmod.fetch_quotes()
                quotes.update(data)
            except Exception as e:
                logger.error(f"Quote stream error in {qmod.__name__}: {e}")

    # 3?? Run ML engines for sizing and confidence
    ml_results = {}
    for mmod in discover_modules(ENGINE_PACKAGES["ml"]):
        if hasattr(mmod, "run"):
            try:
                out = await mmod.run(quotes)
                ml_results.update(out)
            except Exception as e:
                logger.error(f"ML engine error in {mmod.__name__}: {e}")

    # 4?? Apply goal-aware adjustments
    for gmod in discover_modules(ENGINE_PACKAGES["goal"]):
        if hasattr(gmod, "apply"):
            try:
                ml_results = await gmod.apply(ml_results)
            except Exception as e:
                logger.error(f"Goal engine error in {gmod.__name__}: {e}")

    # 5?? Trigger bots based on ml_results
    success_count = 0
    failure_count = 0
    total = len(ml_results)
    for bot_name, params in ml_results.items():
        logger.info(f"--- Bot: {bot_name} | Params: {params} ---")
        if dry_run:
            logger.info(f"[DRY RUN] Would run {bot_name} with {params}")
            continue
        try:
            result = await run_bot_with_params(**params)
            errs = result.get("response", {}).get("errors")
            if result.get("status") == "success" and not errs:
                logger.info(f"? Success: {bot_name}")
                success_count += 1
            else:
                logger.error(f"? Failure: {bot_name}, errors={errs or 'unknown'}")
                failure_count += 1
        except Exception as e:
            logger.error(f"? Exception in {bot_name}: {e}")
            failure_count += 1
        logger.info("=" * 50)

    # 6?? Update positions
    try:
        pmod = importlib.import_module(ENGINE_PACKAGES["position"])
        if hasattr(pmod, "update"):
            await pmod.update(quotes, ml_results)
    except Exception as e:
        logger.error(f"Position tracker error: {e}")

    # 7?? Summary logging
    summary = {
        "timestamp": datetime.utcnow().isoformat(),
        "successes": success_count,
        "failures": failure_count,
        "total": total,
        "dry_run": dry_run,
    }
    os.makedirs("logs", exist_ok=True)
    with open("logs/orchestrator_results.json", "a") as f:
        f.write(json.dumps(summary) + "\n")

    logger.info(f"?? Orchestration complete: {success_count}/{total} succeeded.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SkyStrike orchestration pipeline")
    parser.add_argument("--dry-run", action="store_true", help="Simulate actions without placing orders")
    args = parser.parse_args()
    asyncio.run(run_pipeline(dry_run=args.dry_run))
