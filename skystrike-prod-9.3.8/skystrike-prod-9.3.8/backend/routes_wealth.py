from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter()

class ETFAllocation(BaseModel):
    symbol: str
    allocation: float

@router.get("/api/wealth/etf-allocation", response_model=List[ETFAllocation])
def get_etf_allocation():
    return [
        {"symbol": "VOO", "allocation": 40.0},
        {"symbol": "VTI", "allocation": 30.0},
        {"symbol": "BND", "allocation": 20.0},
        {"symbol": "VXUS", "allocation": 10.0},
    ]

@router.post("/api/wealth/allocate-csp")
def allocate_csp():
    return {"status": "success", "message": "Cash-secured puts allocated as per strategy."}