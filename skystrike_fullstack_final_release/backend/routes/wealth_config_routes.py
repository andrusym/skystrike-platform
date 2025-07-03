from fastapi import APIRouter
core.wealth_utils import load_wealth_config, save_wealth_config

router = APIRouter()

@router.get("/wealth/config")
def get_config():
    return load_wealth_config()

@router.post("/wealth/config")
def save_config(config: dict):
    save_wealth_config(config)
    return {"status": "saved"}
