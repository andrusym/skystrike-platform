# backend/services/ml_engine_service.py

"""
Service layer for ML engine operations:
- Fetching ML scores
- Evaluating ML model status
- Generating combined portfolio recommendations
"""

import logging
from typing import Dict, Any

from backend.engine.ml_engine import load_ml_scores, evaluate_ml_status
from backend.engine.final_recommendation_engine import generate_final_recommendation

logger = logging.getLogger(__name__)

def get_ml_scores() -> Dict[str, Any]:
    """
    Retrieve the latest ML scores for all bots.
    """
    try:
        scores = load_ml_scores()
        logger.debug(f"Retrieved ML scores: {scores}")
        return scores
    except Exception as e:
        logger.error(f"Error retrieving ML scores: {e}")
        raise

def get_ml_status() -> Dict[str, Any]:
    """
    Evaluate the health and status of the ML model.
    """
    try:
        status = evaluate_ml_status()
        logger.debug(f"Evaluated ML status: {status}")
        return status
    except Exception as e:
        logger.error(f"Error evaluating ML status: {e}")
        raise

def get_final_recommendation(user_profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate the final portfolio recommendation by combining ML tuning
    outputs with goal-based portfolio shifts.
    """
    try:
        recommendation = generate_final_recommendation(user_profile)
        logger.debug(f"Generated final recommendation: {recommendation}")
        return recommendation
    except Exception as e:
        logger.error(f"Error generating final recommendation: {e}")
        raise

__all__ = ["get_ml_scores", "get_ml_status", "get_final_recommendation"]
