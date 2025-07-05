# backend/ml/ml_engine.py

"""
Core ML engine functions for loading ML scores and evaluating model status.
"""

import json
import logging
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

# Path to the ML scores file (exported by self-tuning engine)
ML_SCORES_FILE = Path(__file__).parent.parent / "ml_scores.json"

def load_ml_scores() -> dict:
    """
    Load machine learning scores for each bot from a JSON file.
    Returns a dict mapping bot names to their score metadata.
    """
    try:
        with open(ML_SCORES_FILE) as f:
            data = json.load(f)
        logger.debug(f"Loaded ML scores from {ML_SCORES_FILE}: {data}")
        return data
    except FileNotFoundError:
        logger.error(f"ML scores file not found: {ML_SCORES_FILE}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding ML scores JSON: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error loading ML scores: {e}")
        raise

def evaluate_ml_status() -> dict:
    """
    Evaluates the health of the ML model based on scores availability and freshness.
    Returns a dict with status info.
    """
    try:
        scores = load_ml_scores()
        status = {
            "healthy": bool(scores),
            "last_updated": datetime.utcfromtimestamp(ML_SCORES_FILE.stat().st_mtime).isoformat(),
            "timestamp": datetime.utcnow().isoformat()
        }
        logger.debug(f"ML status: {status}")
        return status
    except Exception as e:
        logger.error(f"Failed to evaluate ML status: {e}")
        return {"healthy": False, "error": str(e)}

__all__ = ["load_ml_scores", "evaluate_ml_status"]
