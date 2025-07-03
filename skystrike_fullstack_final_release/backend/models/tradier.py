# backend/models/tradier.py

from pydantic import BaseModel, Field, model_validator
from typing import Literal, Optional, List

class TradierOrderLeg(BaseModel):
    symbol: str
    side: Literal["buy", "sell"]
    quantity: int
    type: Literal["market", "limit", "stop"]
    price: Optional[float] = None
    stop: Optional[float] = None
    option_symbol: Optional[str] = None
    duration: Literal["day", "gtc"] = "day"

class TradierOrderRequest(BaseModel):
    """
    Mirrors the Tradier Place Order spec.
    Single-leg: class=\"equity\" or \"option\" plus symbol, side, quantity, type.
    Multi-leg: class=\"multileg\" plus a non-empty list of legs.
    """
    class_: Literal["equity", "option", "multileg"] = Field(..., alias="class")
    symbol: Optional[str] = None
    side: Optional[Literal["buy", "sell"]] = None
    quantity: Optional[int] = None
    type: Optional[Literal["market", "limit", "stop"]] = None
    price: Optional[float] = None
    stop: Optional[float] = None
    option_symbol: Optional[str] = None
    duration: Literal["day", "gtc"] = "day"
    legs: Optional[List[TradierOrderLeg]] = None

    class Config:
        validate_by_name = True

    @model_validator(mode="after")
    def check_required_fields(cls, model):
        if model.class_ == "multileg":
            if not model.legs:
                raise ValueError("legs must be provided for multileg orders")
        else:
            missing = [
                name for name in ("symbol", "side", "quantity", "type")
                if getattr(model, name) is None
            ]
            if missing:
                raise ValueError(f"Missing fields for single-leg order: {', '.join(missing)}")
        return model
