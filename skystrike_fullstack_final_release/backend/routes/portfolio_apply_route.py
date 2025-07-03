# routes/portfolio_apply_route.py

from fastapi import APIRouter
import json
from datetime import datetime
from backend.routes.portfolio_final_routes import final_portfolio_recommendation

router = APIRouter(prefix="/portfolio")

@router.post("/apply-recommendation")
def apply_recommendation():
    try:
        rec = final_portfolio_recommendation()
        with open("bot_config.json", "w") as f:
            json.dump(rec["adjusted_allocation"], f, indent=2)
        return {
            "status": "applied",
            "timestamp": datetime.utcnow().isoformat(),
            "applied": rec["adjusted_allocation"]
        }
    except Exception as e:
        return {"error": str(e)}
