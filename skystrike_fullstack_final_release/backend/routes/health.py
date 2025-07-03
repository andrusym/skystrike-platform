from fastapi import APIRouter
import os
import requests
import datetime
from sqlite3 import connect
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/api/health")
def health_check():
    status = {
        "database": "ok",
        "tradier": "ok",
        "mlEngine": "online"
    }

    # DB Check
    try:
        conn = connect("skystrike.db")
        conn.execute("SELECT 1")
        conn.close()
    except:
        status["database"] = "down"

    # Tradier check
    try:
        token = os.getenv("TRADIER_TOKEN")
        account_id = os.getenv("TRADIER_ACCOUNT_ID")
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        response = requests.get(
            f"https://api.tradier.com/v1/accounts/{account_id}/balances",
            headers=headers,
            timeout=5
        )
        if not response.ok:
            status["tradier"] = "error"
    except:
        status["tradier"] = "down"

    return {
        "status": "ok" if all(v == "ok" or v == "online" for v in status.values()) else "degraded",
        "components": status,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
