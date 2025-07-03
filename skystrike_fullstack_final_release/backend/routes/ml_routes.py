from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/ml/status")
def get_ml_status():
    return {
        "status": "online",
        "confidence_threshold": 0.6,
        "last_tune": datetime.utcnow().isoformat() + "Z",
        "cooldown_active": False
    }
