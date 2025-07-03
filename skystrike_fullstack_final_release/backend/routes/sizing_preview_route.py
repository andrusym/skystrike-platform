# backend/routes/sizing_preview_route.py

import inspect
import asyncio
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from backend.auth import get_current_user, User
from backend.services.portfolio import preview_sizing  # your sizing logic

router = APIRouter(prefix="/api/portfolio", tags=["portfolio"])


class SizingPreviewRequest(BaseModel):
    account_size: float
    # add any other inputs your preview_sizing function requires,
    # e.g. goal: str, cash_on_hand: float, etc.


@router.post("/sizing-preview", summary="Preview portfolio sizing recommendations")
async def sizing_preview_endpoint(
    req: SizingPreviewRequest,
    user: User = Depends(get_current_user)
):
    """
    Returns a sizing recommendation per bot based on the user's account size and goal.
    """
    try:
        # Call your core sizing function
        result = preview_sizing(account_size=req.account_size, user=user)
        # If it's async, await it
        if inspect.isawaitable(result):
            result = await result
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
