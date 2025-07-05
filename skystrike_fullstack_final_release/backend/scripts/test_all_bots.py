#!/usr/bin/env python3
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))

import asyncio
import json
import logging
from datetime import datetime
from backend.submit_order import run_bot_with_params

# configure root logger from env
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=LOG_LEVEL, format="%(message)s")
logger = logging.getLogger(__name__)

# silence all the noisy loggers
for noisy in (
    "backend.bots",
    "skystrike.submit",
    "backend.services.option_lookup",
    "httpx",
    "httpcore",
):
    logging.getLogger(noisy).setLevel(logging.ERROR)

BOTS = [
    ("ironcondor", "SPY", 1, 1),
    ("kingcondor",  "SPY", 1, 1),
    ("spread",     "SPY", 1, 1),
    ("csp",        "SPY", 1, 1),
    ("wheel",      "SPY", 1, 1),
    ("trend",      "SPY", 1, 1),
    ("replicator", "SPY", 1, 1),
    ("scalper",    "SPY", 1, 1),
    ("momentumbot","SPY", 1, 1),
    ("straddlebot","SPY", 1, 1),
    ("squeezehunter","SPY",1, 1),
    ("copybot",    "SPY", 1, 1),
    ("calendarbot","SPY", 1, 1),
    ("breakoutbot","SPY", 1, 1),
    ("earningsbot","SPY", 1, 1),
    ("volharvest", "SPY", 1, 1),
    ("gammafly",   "SPY", 1, 1),
    ("ratioflybot","SPY", 1, 1),
    ("dcabot",     "SPY", 1, 1),
    ("pairstrader","SPY", 1, 1),
    ("equity_buy", "QQQ", 1, 0),
]

async def main():
    success_count = 0
    failure_count = 0

    for bot_name, ticker, contracts, dte in BOTS:
        logger.info(f"--- Running {bot_name} ---")
        try:
            result = await run_bot_with_params(bot_name, ticker, contracts, dte, mode="paper")
            # if Tradier returned a top-level "errors" blob, treat it as a failure
            errs = result.get("response", {}).get("errors")
            if result.get("status") == "success" and not errs:
                logger.info("? Success: %s", result)
                success_count += 1
            else:
                logger.error("? Failed: %s", result)
                if errs:
                    logger.error("   API errors: %s", errs)
                failure_count += 1

        except Exception as e:
            logger.error("? Exception in %s: %s", bot_name, e)
            failure_count += 1

        # separator between bots
        logger.info("=" * 40)

    logger.info(
        "?? Summary: %d succeeded, %d failed out of %d total bots.",
        success_count,
        failure_count,
        len(BOTS),
    )

    summary = {
        "timestamp": datetime.utcnow().isoformat(),
        "successes": success_count,
        "failures": failure_count,
        "total": len(BOTS),
    }
    os.makedirs("logs", exist_ok=True)
    with open("logs/bot_test_results.json", "a") as f:
        f.write(json.dumps(summary) + "\n")

if __name__ == "__main__":
    asyncio.run(main())
