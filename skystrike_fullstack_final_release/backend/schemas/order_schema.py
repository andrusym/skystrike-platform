from pydantic import BaseModel

class Order(BaseModel):
    ticker: str
    strategy: str
    contracts: int
