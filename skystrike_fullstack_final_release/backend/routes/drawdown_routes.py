from fastapi import APIRouter

router = APIRouter()

@router.get("/status")
def get_drawdown_protection():
    return {"status": "armed", "threshold": -10.0, "current_drawdown": -3.2}