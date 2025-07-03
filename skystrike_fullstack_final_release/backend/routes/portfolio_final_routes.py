from fastapi import APIRouter

router = APIRouter(prefix="/portfolio")

@router.get("/final-recommendation")
def final_portfolio_recommendation():
    return {
        "adjusted_allocation": {
            "ironcondor": 1,
            "wheel": 0,
            "trend": 0
        }
    }
