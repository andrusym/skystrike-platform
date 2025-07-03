
from fastapi import APIRouter
from datetime import datetime

router = APIRouter(prefix="/wealth")

@router.get("/holdings")
def get_wealth_holdings():
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "cash": 18500,
        "etfs": {
            "VTI": {"shares": 12, "price": 225.67},
            "SCHD": {"shares": 20, "price": 78.45},
            "JEPI": {"shares": 15, "price": 56.12}
        }
    }
