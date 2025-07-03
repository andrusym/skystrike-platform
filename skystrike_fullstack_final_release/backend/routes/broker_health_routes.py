from fastapi import APIRouter
services.tradier_client import ping_tradier

router = APIRouter()

@router.get("/broker/health")
def broker_health():
    try:
        latency_ms = ping_tradier()
        return {"ping_ms": latency_ms}
    except Exception as e:
        return {"error": str(e)}
