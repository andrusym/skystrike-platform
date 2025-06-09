from fastapi import APIRouter
from routes_wealth import router as wealth_router

router = APIRouter()

router.include_router(wealth_router)


from fastapi import APIRouter, HTTPException
from strategy_engine import StrategyEngine
from dashboard import generate_dashboard_summary

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "OK", "message": "SkyStrike API is running"}

@router.get("/dashboard")
def get_dashboard():
    summary = generate_dashboard_summary()
    return summary

@router.post("/trade/start")
def start_trade(ticker: str, strategy_type: str = "iron_condor", capital: float = 10000):
    config = {
        "min_score": 0.6
    }
    try:
        engine = StrategyEngine(
            ticker=ticker,
            capital=capital,
            strategy_type=strategy_type,
            config=config,
            mode="paper"
        )
        result = engine.run()
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from routes_backtest import router as backtest_router
router.include_router(backtest_router)

from replication_api import router as replication_router
router.include_router(replication_router)
