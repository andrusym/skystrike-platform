# backend/routes/wealth_log_route.py

from fastapi import APIRouter
from fastapi.responses import JSONResponse
import os
import json

router = APIRouter()

LOG_FILE_PATH = os.path.join("logs", "wealth_cron.log")

@router.get("/wealth/log")
async def read_wealth_log():
    try:
        if not os.path.exists(LOG_FILE_PATH):
            return JSONResponse(content={"log": "[Log file not found]"}, status_code=404)

        with open(LOG_FILE_PATH, "r") as file:
            lines = file.readlines()[-50:]  # Show last 50 lines
            return {"log": "".join(lines)}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
