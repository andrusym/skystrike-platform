from fastapi import APIRouter

router = APIRouter()

@router.get("/api/backtest/{strategy_name}")
def get_backtest_results(strategy_name: str):
    # Placeholder — replace with real backtest fetch logic
        return {
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
        "strategy": strategy_name,
        "winRate": 72.4,
        "avgProfit": 185.6,
        "maxDrawdown": -640.0,
        "sampleSize": 140
    }
