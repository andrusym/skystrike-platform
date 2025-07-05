# backend/engine/ml_engine.py

import os
import json
from datetime import datetime

ML_STATUS_PATH = "logs/ml_status.json"
ML_SCORES_PATH = "logs/ml_scores.json"


def get_ml_status() -> dict:
    """
    Returns the current ML engine status based on a heartbeat file.
    """
    if not os.path.exists(ML_STATUS_PATH):
        return {
            "status": "unknown",
            "message": "ML status file missing",
            "fallback_active": True,
        }

    try:
        with open(ML_STATUS_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error reading ML status: {str(e)}",
            "fallback_active": True,
        }


def load_ml_scores() -> dict:
    """
    Load latest ML scores for all bots from file.
    """
    if not os.path.exists(ML_SCORES_PATH):
        return {}

    try:
        with open(ML_SCORES_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        return {
            "error": f"Could not load ml_scores.json: {str(e)}"
        }


def evaluate_ml_status() -> str:
    """
    Quick logic to determine system status from ML heartbeat.
    """
    status = get_ml_status()
    if status.get("status") == "healthy" and not status.get("fallback_active"):
        return "? ML ACTIVE"
    elif status.get("fallback_active"):
        return "?? ML FALLBACK"
    else:
        return "? ML UNKNOWN"
