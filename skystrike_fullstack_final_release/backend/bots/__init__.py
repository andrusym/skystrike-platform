# backend/bots/runner.py

import pkgutil
import importlib
import logging
import os

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def load_all_bots():
    build_map = {}
    pkg_dir = os.path.dirname(__file__)

    for finder, module_name, ispkg in pkgutil.iter_modules([pkg_dir]):
        # skip private modules/helpers
        if module_name.startswith("_") or module_name in ("runner", "hybrid_bot"):
            continue

        try:
            mod = importlib.import_module(f"backend.bots.{module_name}")
            build_fn = getattr(mod, "build_order", None)
            if not callable(build_fn):
                logger.warning(f"[bots] ?? No build_order() in {module_name}")
                continue

            # register under the file name…
            build_map[module_name] = build_fn

            # …and also register under the no-underscore alias
            alias = module_name.replace("_", "")
            if alias != module_name:
                build_map[alias] = build_fn

            logger.info(f"[bots] ? Loaded {module_name} (alias: {alias})")

        except Exception as e:
            logger.error(f"[bots] ? Failed to import {module_name}: {e}")

    return build_map

BUILD_MAP = load_all_bots()


def build_order(bot_name: str, ticker: str, contracts: int, dte: int, mode: str, confidence: float = None):
    """
    Dispatch to the appropriate bot's build_order function.
    """
    try:
        fn = BUILD_MAP[bot_name]
    except KeyError:
        raise ValueError(f"Bot '{bot_name}' not supported.")
    return fn(ticker=ticker, contracts=contracts, dte=dte, mode=mode)
