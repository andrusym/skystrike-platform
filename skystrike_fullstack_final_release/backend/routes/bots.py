# routes/bots.py

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
services.auth import verify_token
from typing import Optional

# ? Import all bot modules
from bots import (
    iron_condor,
    king_condor,
    wheel,
    csp,
    trend,
    replicator,
    gridbot,
    dcabot,
    scalper,
    pairstrader,
    momentumbot,
    copybot
)

router = APIRouter()

# --- Request Model ---
class BotTriggerRequest(BaseModel):
    ticker: str
    contracts: int = 1

# --- Bot Trigger Registry ---
BOT_RUNNERS = {
    "ironcondor": iron_condor.run_bot_with_params,
    "kingcondor": king_condor.run_bot_with_params,
    "wheel": wheel.run_bot_with_params,
    "csp": csp.run_bot_with_params,
    "trend": trend.run_bot_with_params,
    "replicator": replicator.run_bot_with_params,
    "gridbot": gridbot.run_bot_with_params,
    "dcabot": dcabot.run_bot_with_params,
    "scalper": scalper.run_bot_with_params,
    "pairstrader": pairstrader.run_bot_with_params,
    "momentumbot": momentumbot.run_bot_with_params,
    "copybot": copybot.run_bot_with_params,
}

# --- General Bot Trigger Endpoint ---
@router.post("/api/bots/trigger/{bot_name}")
async def trigger_bot(
    bot_name: str,
    payload: BotTriggerRequest,
    user=Depends(verify_token)
):
    bot_name = bot_name.lower()

    if bot_name not in BOT_RUNNERS:
        raise HTTPException(status_code=404, detail=f"Bot '{bot_name}' not found")

    try:
        run_bot = BOT_RUNNERS[bot_name]
        result = await run_bot(bot_name, payload.ticker, payload.contracts)
        return {
            "status": "order placed",
            "strategy": bot_name,
            "ticker": payload.ticker,
            "contracts": payload.contracts,
            "broker_response": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bot '{bot_name}' failed: {str(e)}")

# --- Optional: List All Available Bots ---
@router.get("/api/bots/list")
def list_bots():
    return {"available_bots": list(BOT_RUNNERS.keys())}
