# backend/ml/ml_engine.py

"""
Core ML engine with dynamic plugin loading and static JSON fallback.
"""

import pkgutil
import importlib
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)

# Path to the ML scores file (exported by self-tuning engine)
ML_SCORES_FILE = Path(__file__).parent.parent / "data" / "ml_scores.json"


def load_ml_scores() -> Dict[str, Any]:
    """
    Load machine-learning scores for each bot from a JSON file.
    Returns a dict mapping bot names to their score metadata.
    """
    try:
        with open(ML_SCORES_FILE) as f:
            data = json.load(f)
        logger.debug(f"Loaded ML scores from {ML_SCORES_FILE}: {data}")
        return data
    except FileNotFoundError:
        logger.error(f"ML scores file not found: {ML_SCORES_FILE}")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding ML scores JSON: {e}")
        return {}
    except Exception as e:
        logger.error(f"Unexpected error loading ML scores: {e}")
        return {}


def evaluate_ml_status() -> Dict[str, Any]:
    """
    Evaluate health of the ML model based on scores availability and freshness.
    Returns a status dict.
    """
    scores = load_ml_scores()
    healthy = bool(scores)
    last_updated = None
    try:
        last_updated = datetime.utcfromtimestamp(ML_SCORES_FILE.stat().st_mtime).isoformat()
    except Exception:
        logger.warning(f"Could not stat ML scores file at {ML_SCORES_FILE}")
    status = {
        "healthy": healthy,
        "last_updated": last_updated,
        "timestamp": datetime.utcnow().isoformat(),
    }
    logger.debug(f"ML status: {status}")
    return status


async def run(quotes: Dict[str, Any]) -> Dict[str, Any]:
    """
    Discover every plugin module under backend/ml/ (except this one),
    call its async run(quotes), and merge results.
    If no plugins found or all fail, fallback to JSON ml_scores.
    """
    results: Dict[str, Any] = {}

    # Discover plugin modules
    pkg = importlib.import_module(__name__)
    base_pkg = pkg.__package__  # "backend.ml"
    for finder, name, is_pkg in pkgutil.iter_modules(pkg.__path__):
        if is_pkg or name.startswith("_") or name == "ml_engine":
            continue

        full_name = f"{base_pkg}.{name}"
        try:
            mod = importlib.import_module(full_name)
        except Exception as e:
            logger.error(f"Failed to import ML plugin {full_name}: {e}")
            continue

        run_fn = getattr(mod, "run", None)
        if not callable(run_fn):
            logger.debug(f"Skipping {full_name}: no run(quotes)")
            continue

        try:
            out = await run_fn(quotes)
            if isinstance(out, dict):
                results.update(out)
            else:
                logger.error(f"Plugin {full_name}.run did not return dict")
        except Exception as e:
            logger.error(f"Error in ML plugin {full_name}.run: {e}")

    # Fallback to static JSON if none of the plugins returned anything
    if not results:
        logger.info("No ML plugins returned results; falling back to ml_scores.json")
        static_scores = load_ml_scores()
        for bot, spec in static_scores.items():
            # Ensure correct type/keys
            try:
                results[bot] = {
                    "bot_name":  bot,
                    "symbol":    spec["symbol"],
                    "contracts": int(spec.get("contracts", 1)),
                    "dte":       int(spec.get("dte", 1)),
                    "mode":      spec.get("mode", "paper"),
                }
            except Exception as e:
                logger.error(f"Invalid spec for bot {bot} in ml_scores.json: {e}")

    return results


__all__ = ["load_ml_scores", "evaluate_ml_status", "run"]
