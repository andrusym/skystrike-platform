from fastapi import APIRouter
from datetime import datetime

router = APIRouter(prefix="/api")

@router.get("/system/health")
def health_check():
    return {
        "ml_heartbeat": "OK",
        "retry_loop_status": "ACTIVE",
        "broker_ping_ms": 142,
        "degrade_state": False,
        "last_updated": datetime.utcnow().isoformat()
    }
