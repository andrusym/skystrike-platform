from fastapi import APIRouter, Request
services.tradier_client import get_order_history

router = APIRouter()

@router.get("/history")
def order_history(request: Request):
    token = request.headers.get("X-Broker-Token")
    return get_order_history(token_override=token)