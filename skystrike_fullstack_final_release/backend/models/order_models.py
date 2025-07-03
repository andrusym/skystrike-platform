from pydantic import BaseModel, Field
from typing import List

class OrderLeg(BaseModel):
    symbol: str
    side: str
    quantity: int
    type: str
    duration: str

class PlaceOrderRequest(BaseModel):
    class_: str = Field(alias="class")
    legs: List[OrderLeg]

    class Config:
        allow_population_by_field_name = True
