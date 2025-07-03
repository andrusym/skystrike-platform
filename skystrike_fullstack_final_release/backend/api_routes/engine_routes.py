from fastapi import APIRouter, HTTPException
from engine.final_recommendation_engine import generate_final_recommendation
from engine.self_tuning_engine import SelfTuningEngine
from engine.ml_status import get_ml_status
from engine.bot_entry_engine import execute_bot
from engine.strategy_config import get_all_bot_configs

router = APIRouter(prefix="/engine", tags=["engine"])

@router.get("/final-recommendation")
def final_recommendation():
    try:
        return generate_final_recommendation()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/self-tune")
def self_tune():
    try:
        engine = SelfTuningEngine(strategies=list(get_all_bot_configs().keys()))
        engine.tune_all()
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
def ml_status():
    return get_ml_status()

@router.post("/trigger/{bot_name}")
def trigger_bot(bot_name: str):
    try:
        return execute_bot(bot_name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bot error: {str(e)}")
