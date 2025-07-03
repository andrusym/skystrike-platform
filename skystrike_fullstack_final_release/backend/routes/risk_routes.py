from fastapi import APIRouter
from fastapi.responses import JSONResponse
from datetime import datetime
from backend.services.correlation_monitor import check_correlation
from backend.services.macro_throttle import get_macro_throttle_status
from backend.services.drawdown_guard import get_drawdown_status

router = APIRouter(prefix="/risk")

@router.get("/metrics")
def get_risk_metrics():
    try:
        return {
            "status": "ok",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.get("/correlation")
def correlation():
    return check_correlation()

@router.get("/throttle")
def throttle():
    return get_macro_throttle_status()

@router.get("/drawdown")
def drawdown():
    return get_drawdown_status()
