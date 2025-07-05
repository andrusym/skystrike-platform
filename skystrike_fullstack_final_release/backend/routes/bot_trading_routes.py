from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from backend.utils.auth import verify_token
from backend.submit_order import BUILD_MAP as BOT_RUNNERS

router = APIRouter()

class BotTriggerRequest(BaseModel):
    ticker: str
    contracts: int = 1

@router.post("/bots/trigger/{bot_name}")
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

@router.get("/bots/list")
def list_bots():
    return {"available_bots": list(BOT_RUNNERS.keys())}
