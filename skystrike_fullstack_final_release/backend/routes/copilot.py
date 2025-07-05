# backend/routes/copilot.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

# Correct import path for the Copilot engine
from ..engine.copilot_engine import get_top_recommendation
from ..auth import get_current_user, User

router = APIRouter(
    prefix="/api/copilot",
    tags=["copilot"],
)

@router.get("/guidance/{ticker}", summary="Get AI trade guidance for a ticker")
async def copilot_guidance(ticker: str, current_user: User = Depends(get_current_user)):
    """
    Fetch top trade recommendation and rationale from the Copilot engine.
    """
    try:
        recommendation = get_top_recommendation(ticker)
        return JSONResponse(content={"recommendation": recommendation})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
