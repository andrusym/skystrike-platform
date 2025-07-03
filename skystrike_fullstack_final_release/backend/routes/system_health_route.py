from fastapi import APIRouter
from datetime import datetime
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/system/health")
def get_system_health():
    try:
        return {
            "ml_heartbeat": "OK",
            "retry_loop_status": "ACTIVE",
            "broker_ping_ms": 156,
            "degrade_state": False,
            "last_updated": datetime.utcnow().isoformat() + "Z"
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
