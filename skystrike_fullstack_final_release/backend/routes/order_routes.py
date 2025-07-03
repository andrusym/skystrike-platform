from fastapi import APIRouter, Request, HTTPException, Depends
from backend.submit_order import run_bot_with_params
from backend.services.log_writer import append_log
from backend.dependencies.auth import get_current_user
from backend.config.bot_config import get_enabled_bots
from backend.engines.ml_scoring import get_bot_confidence

router = APIRouter(prefix="/api/orders", tags=["orders"])

@router.post("/place")
async def place_order_api(request: Request, user=Depends(get_current_user)):
    try:
        data = await request.json()
        bot = data["bot"]
        ticker = data["ticker"]
        contracts = data["contracts"]
        confidence = data.get("confidence", 1.0)
        dte = data.get("dte", 0)

        # Call unified submit_order logic
        result = run_bot_with_params(bot=bot, ticker=ticker, contracts=contracts, dte=dte)

        append_log("orders", {
            "bot": bot,
            "ticker": ticker,
            "contracts": contracts,
            "confidence": confidence,
            "dte": dte,
            "response": result
        })

        return {"status": "success", "order": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Order placement failed: {str(e)}")


@router.post("/place_all")
async def place_all_orders(user=Depends(get_current_user)):
    enabled_bots = get_enabled_bots()
    results = {}

    for bot in enabled_bots:
        try:
            confidence = get_bot_confidence(bot)
            ticker = "SPX" if "condor" in bot else "SPY"
            dte = 0
            contracts = 1  # Can be made dynamic later

            result = run_bot_with_params(bot=bot, ticker=ticker, contracts=contracts, dte=dte)

            append_log("orders", {
                "bot": bot,
                "ticker": ticker,
                "contracts": contracts,
                "confidence": confidence,
                "dte": dte,
                "response": result
            })

            results[bot] = {"status": "success", "order": result}
        except Exception as e:
            results[bot] = {"error": str(e)}

    return {"status": "complete", "orders": results}
