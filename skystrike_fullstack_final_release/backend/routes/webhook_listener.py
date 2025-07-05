import json
from fastapi import APIRouter, Request, HTTPException

router = APIRouter()

@router.post("/api/webhook")
async def receive_webhook(request: Request):
    try:
        payload = await request.json()
        bot = payload.get("bot")
        ticker = payload.get("ticker")
        contracts = payload.get("contracts", 1)
        dte = payload.get("dte", 0)

        if not bot or not ticker:
            raise HTTPException(status_code=400, detail="Missing bot or ticker")

        # Placeholder logic – replace with actual trigger
        print(f"Webhook received: {bot}, {ticker}, {contracts} contracts, DTE={dte}")
        return {"status": "accepted", "bot": bot, "ticker": ticker, "contracts": contracts, "dte": dte}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing webhook: {e}")