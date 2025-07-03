from fastapi import APIRouter, HTTPException
from engine.final_recommendation_engine import generate_final_recommendation
from engine.goal_aware_shift_engine import shift_allocation_goal

router = APIRouter(prefix="/portfolio", tags=["portfolio"])

@router.get("/recommendation")
def recommendation():
    try:
        return generate_final_recommendation()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/adjusted-recommendation")
def adjusted(goal: str = "balanced"):
    try:
        return shift_allocation_goal(goal)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
