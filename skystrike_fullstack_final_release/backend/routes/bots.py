# backend/routes/bots.py

import inspect
from typing import List, Any, Dict

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from ..auth import get_current_user, User
from ..submit_order import BUILD_MAP as BOT_RUNNERS

router = APIRouter(
    prefix="/api/bots",
    tags=["bots"],
)

class BotTriggerRequest(BaseModel):
    ticker: str
    contracts: int = 1

@router.get(
    "/list",
    response_model=List[str],
    summary="List all available bots",
)
def list_bots(current_user: User = Depends(get_current_user)) -> List[str]:
    """
    Returns the list of bot names you can trigger.
    """
    return list(BOT_RUNNERS.keys())

@router.post(
    "/trigger/{bot_name}",
    response_model=Dict[str, Any],
    summary="Trigger a bot execution",
)
async def trigger_bot(
    bot_name: str,
    payload: BotTriggerRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Executes the specified bot by name with your ticker & contract count.
    """
    key = bot_name.lower()
    runner = BOT_RUNNERS.get(key)
    if not runner:
        raise HTTPException(status_code=404, detail=f"Bot '{bot_name}' not found")

    try:
        # Support both async and sync runners
        if inspect.iscoroutinefunction(runner):
            result = await runner(key, payload.ticker, payload.contracts)
        else:
            result = runner(key, payload.ticker, payload.contracts)

        return {
            "status": "success",
            "strategy": key,
            "ticker": payload.ticker,
            "contracts": payload.contracts,
            "broker_response": result,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Bot '{key}' failed: {e}",
        )
