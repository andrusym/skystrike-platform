from fastapi import APIRouter

router = APIRouter()

@router.get("/vix")
def get_vix_info():
    return {"vix": 13.5, "regime": "calm"}