from pydantic import BaseModel

class Order(BaseModel):
    symbol: str
    side: str
    quantity: int
    type: str
    duration: str
    price: float | None = None  # Optional for market orders
