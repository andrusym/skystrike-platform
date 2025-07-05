# backend/engine/bot_entry_engine.py

import logging
import asyncio

logger = logging.getLogger(__name__)

# Map bot names to their build functions
BOT_BUILDERS = {
    "ironcondor":  ("backend.bots.iron_condor",  "build_order"),
    "kingcondor":  ("backend.bots.kingcondor",   "build_order"),
    "spread":      ("backend.bots.spread",       "build_order"),
    "csp":         ("backend.bots.csp",          "build_order"),
    "wheel":       ("backend.bots.wheel",        "build_order"),
    "trend":       ("backend.bots.trend",        "build_order"),
    "replicator":  ("backend.bots.replicator",   "build_order"),
    "copybot":     ("backend.bots.copybot",      "build_order"),
    "dcabot":      ("backend.bots.dcabot",       "build_order"),
    "gridbot":     ("backend.bots.gridbot",      "build_order"),
    "momentumbot": ("backend.bots.momentumbot",  "build_order"),
    "scalper":     ("backend.bots.scalper",      "build_order"),
    "pairstrader": ("backend.bots.pairstrader",  "build_order"),
    # add additional bots here...
}

async def run_all_bots():
    """
    Execute each bot in turn, building its order payload and submitting it.
    Returns a dict mapping bot_name -> result (or None on failure).
    """
    from backend.submit_order import run_bot_with_params

    results = {}
    # default args for a full orchestration run
    defaults = {"ticker": "SPY", "contracts": 1, "dte": 7, "mode": None}

    for bot_name, (module_path, fn_name) in BOT_BUILDERS.items():
        try:
            logger.info(f"Building order for bot: {bot_name}")
            module = __import__(module_path, fromlist=[fn_name])
            build_fn = getattr(module, fn_name)

            # handle both sync and async build_order functions
            if asyncio.iscoroutinefunction(build_fn):
                order_payload = await build_fn(**defaults)
            else:
                order_payload = build_fn(**defaults)

            logger.info(f"Submitting order for {bot_name}: {order_payload}")
            # run_bot_with_params is async
            outcome = await run_bot_with_params(bot_name, order_payload)
            results[bot_name] = outcome

        except Exception:
            logger.exception(f"Failed to run bot: {bot_name}")
            results[bot_name] = None

    return results
