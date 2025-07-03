
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from backend.services.replication_api import run_replication
from datetime import datetime

router = APIRouter(prefix="/replication")

@router.post("/run")
def replicate():
    try:
        result = run_replication()
        return {"status": "started", "result": result}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
