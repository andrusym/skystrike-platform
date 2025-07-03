from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
auth import verify_token
services.tradier_service import preview_order
from models.order import Order

router = APIRouter()

@router.post("/api/orders/preview")
async def order_preview(request: Request, user=Depends(verify_token)):
    try:
        data = await request.json()
        order = Order(**data)
        preview_response = await preview_order(order)
        return JSONResponse(content=preview_response)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
