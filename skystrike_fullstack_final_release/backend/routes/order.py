from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from backend.utils.auth_utils import get_current_user, User
from backend.submit_order import BUILD_MAP
from backend.services.tradier_client import TradierClient

router = APIRouter()


class OrderRequest(BaseModel):
    bot: str
    ticker: str
    contracts: int
    dte: int


@router.post("/api/orders/place")
def place_order(order: OrderRequest, user: User = Depends(get_current_user)):
    try:
        # Determine mode from JWT user (default to 'paper' if not present)
        mode = getattr(user, "tradier_mode", "paper").lower()

        # Retrieve build_order function for the specified bot
        build_order = BUILD_MAP.get(order.bot.lower())
        if not build_order:
            raise HTTPException(status_code=400, detail=f"Unknown bot: {order.bot}")

        # Build and submit order
        order_spec = build_order(
            bot=order.bot,
            ticker=order.ticker,
            contracts=order.contracts,
            dte=order.dte,
            mode=mode
        )

        client = TradierClient(mode)
        response = client.submit_order(order_spec)
        return response

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Order placement failed: {str(e)}")
