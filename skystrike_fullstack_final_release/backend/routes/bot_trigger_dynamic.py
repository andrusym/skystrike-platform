# backend/routes/bot_trigger_dynamic.py

import importlib
import inspect
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from backend.auth import get_current_user, User
import backend.bots as bots_pkg

router = APIRouter()
BOT_NAMES = getattr(bots_pkg, "__all__", [])


class BotRequest(BaseModel):
    ticker: str
    contracts: int = 1


@router.get("/bots", summary="List available bots")
async def list_bots(user: User = Depends(get_current_user)):
    """
    Returns the list of all bot names you can trigger.
    """
    return {"available_bots": BOT_NAMES}


@router.post("/bots/{bot_name}/run", summary="Trigger a bot")
async def trigger_bot(
    bot_name: str,
    bot_request: BotRequest,
    user: User = Depends(get_current_user)
):
    """
    Runs the specified bot by name with given parameters.
    """
    if bot_name not in BOT_NAMES:
        raise HTTPException(status_code=404, detail=f"Bot '{bot_name}' not found.")

    module = importlib.import_module(f"{bots_pkg.__name__}.{bot_name}")
    run_fn = getattr(module, "run_bot_with_params", None)
    if not callable(run_fn):
        raise HTTPException(
            status_code=500,
            detail=f"Bot '{bot_name}' missing a callable run_bot_with_params()"
        )

    # call sync or async
    result = run_fn(bot_name, bot_request.ticker, bot_request.contracts)
    if inspect.isawaitable(result):
        result = await result

    return {"bot": bot_name, "result": result}
