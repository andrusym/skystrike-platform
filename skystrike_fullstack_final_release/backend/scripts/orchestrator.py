#!/usr/bin/env python3
# coding: utf-8

import os
import pkgutil
import importlib
import asyncio
import logging
import json
import argparse
import sys
from datetime import datetime
from backend.submit_order import run_bot_with_params

# Configure logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=LOG_LEVEL, format="%(message)s")
logger = logging.getLogger(__name__)

ENGINE_DIR = "backend.engine"
ML_DIR     = "backend.ml"
import_errors = []

def discover_modules(pkg_name):
    """
    Import pkg_name, then import every .py module directly under it.
    Skip flat modules that aren't packages.
    Record import failures to import_errors.
    """
    modules = []
    try:
        pkg = importlib.import_module(pkg_name)
    except Exception as e:
        import_errors.append((pkg_name, e))
        return modules

    path = getattr(pkg, "__path__", None)
    if not path:
        logger.warning(f"?? {pkg_name} is not a package — skipping")
        return modules

    for finder, name, is_pkg in pkgutil.iter_modules(path):
        if is_pkg or name.startswith("_"):
            continue
        full = f"{pkg_name}.{name}"
        try:
            mod = importlib.import_module(full)
            modules.append(mod)
        except Exception as e:
            import_errors.append((full, e))
    return modules

async def run_pipeline(dry_run=False):
    # 1) Discover engine and ML modules
    logger.info("Scanning engine modules...")
    engines = discover_modules(ENGINE_DIR)

    logger.info("Scanning ML modules...")
    mlmods = discover_modules(ML_DIR)

    # 2) Fail fast on import errors
    if import_errors:
        logger.error("IMPORT ERRORS:")
        for name, err in import_errors:
            logger.error("  - %s: %s", name, err)
        sys.exit(1)

    # 3) Classify by capability
    filters      = [m for m in engines if hasattr(m, "is_trading_day")]
    quote_stream = [m for m in engines if hasattr(m, "fetch_quotes")]
    goals        = [m for m in engines if hasattr(m, "apply")]
    updaters     = [m for m in engines if hasattr(m, "update")]
    ml_engines   = [m for m in mlmods if hasattr(m, "run")]

    logger.info("Filters: %s", [m.__name__ for m in filters])
    logger.info("Quote streams: %s", [m.__name__ for m in quote_stream])
    logger.info("Goals: %s", [m.__name__ for m in goals])
    logger.info("Updaters: %s", [m.__name__ for m in updaters])
    logger.info("ML engines: %s", [m.__name__ for m in ml_engines])

    # 4) Market-day filter
    for mod in filters:
        if not await mod.is_trading_day():
            logger.info("Not a trading day. Exiting.")
            return

    # 5) Fetch quotes
    quotes = {}
    for mod in quote_stream:
        try:
            data = await mod.fetch_quotes()
            quotes.update(data)
        except Exception as e:
            logger.error("Error in fetch_quotes(%s): %s", mod.__name__, e)

    # 6) Run ML
    ml_results = {}
    for mod in ml_engines:
        try:
            out = await mod.run(quotes)
            ml_results.update(out)
        except Exception as e:
            logger.error("Error in ML run(%s): %s", mod.__name__, e)

    # 7) Apply goals
    for mod in goals:
        try:
            ml_results = await mod.apply(ml_results)
        except Exception as e:
            logger.error("Error in apply(%s): %s", mod.__name__, e)

    # 8) Trigger bots
    total = len(ml_results)
    logger.info("Will run %d bots: %s", total, list(ml_results.keys()))
    success = failure = 0

    for bot, params in ml_results.items():
        logger.info("Bot=%s params=%s", bot, params)
        if dry_run:
            logger.info("[DRY RUN] skip %s", bot)
            continue
        try:
            res = await run_bot_with_params(**params)
            errs = res.get("response", {}).get("errors")
            if res.get("status") == "success" and not errs:
                logger.info("Success: %s", bot)
                success += 1
            else:
                logger.error("Failure: %s errors=%s", bot, errs or "unknown")
                failure += 1
        except Exception as e:
            logger.error("Exception in %s: %s", bot, e)
            failure += 1

    # 9) Update positions
    for mod in updaters:
        try:
            await mod.update(quotes, ml_results)
        except Exception as e:
            logger.error("Error in update(%s): %s", mod.__name__, e)

    # 10) Summary
    summary = {
        "timestamp": datetime.utcnow().isoformat(),
        "dry_run":   dry_run,
        "total":     total,
        "success":   success,
        "failure":   failure,
    }
    os.makedirs("logs", exist_ok=True)
    with open("logs/orchestrator_results.json", "a") as f:
        f.write(json.dumps(summary) + "\n")

    logger.info("Done: %d/%d succeeded", success, total)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true", help="simulate only")
    args = p.parse_args()
    asyncio.run(run_pipeline(dry_run=args.dry_run))
