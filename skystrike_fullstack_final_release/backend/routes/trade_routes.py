from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import os
import json

router = APIRouter()

LOG_PATH = "data/trade_log.json"

@router.get("/trades")
def get_trades():
    try:
        if not os.path.exists(LOG_PATH):
            return []

        with open(LOG_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
