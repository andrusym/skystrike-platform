# backend/bots/runner.py

import pkgutil
import importlib
from typing import Callable, Dict
from backend.config import settings

# Build a registry of all bot build_order functions
BOT_BUILDERS: Dict[str, Callable] = {}

# Import the package so we can walk its __path__
import backend.bots as bots_pkg

for finder, module_name, ispkg in pkgutil.iter_modules(bots_pkg.__path__):
    # skip private modules or this runner itself
    if module_name.startswith("_") or module_name in ("runner", "hybrid_bot"):
        continue

    module = importlib.import_module(f"backend.bots.{module_name}")
    build_fn = getattr(module, "build_order", None)
    if not callable(build_fn):
        continue

    # register under the exact module name
    BOT_BUILDERS[module_name] = build_fn

    # also register under its no-underscore alias ("ironcondor" ? "iron_condor")
    alias = module_name.replace("_", "")
    if alias != module_name:
        BOT_BUILDERS[alias] = build_fn


def build_order(
    bot_name: str,
    ticker: str,
    contracts: int,
    dte: int,
    mode: str,
    confidence: float = None,  # if you were previously passing confidence
) -> Dict:
    """
    Dispatch to the appropriate bot's build_order function.
    """
    try:
        fn = BOT_BUILDERS[bot_name]
    except KeyError:
        raise ValueError(f"Bot '{bot_name}' not supported.")

    # Call the bot's build_order. Most of yours expect: (ticker, contracts, dte, mode)
    # If any expect a different signature, you can adapt here.
    return fn(ticker=ticker, contracts=contracts, dte=dte, mode=mode)
