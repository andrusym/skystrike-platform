
from fastapi import APIRouter
from fastapi.responses import JSONResponse
import json
from datetime import datetime

router = APIRouter(prefix="/bots")

@router.get("/logs")
def get_bot_logs():
    try:
        with open("bot_run_log.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"logs": []}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
