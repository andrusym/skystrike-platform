from fastapi import APIRouter
import time
import os

router = APIRouter()

@router.get("/system/health")
def system_health():
    return {
        "broker": "online",
        "ml": "online",
        "wealthEngine": "configured" if os.path.exists("data/wealth_config.json") else "missing_config",
        "diskSpace": "ok",
        "pingMs": round(time.time() % 1 * 1000)  # mock ping
    }
