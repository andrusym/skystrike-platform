from fastapi import APIRouter, Query
import json

router = APIRouter()

@router.get("/api/copilot/guidance")
def copilot_guidance(ticker: str = Query(...)):
    try:
        with open("ml/ml_scores.json") as f:
            ml_scores = json.load(f)
    except:
        ml_scores = {}

    score = ml_scores.get(ticker.upper(), {})
    return {
        "ticker": ticker.upper(),
        "confidence": score.get("confidence", 0),
        "suggested_action": "trade" if score.get("confidence", 0) > 0.7 else "wait",
        "rationale": "Based on ML confidence score and market signal"
    }