from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/support")
def get_support_status():
    try:
        return {
            "support": "operational",
            "tickets_open": 2,
            "sla_met": True
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
