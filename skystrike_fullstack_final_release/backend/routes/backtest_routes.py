from fastapi import APIRouter
import json
import os

router = APIRouter()

@router.get("/fallback/status")
def get_fallback_status():
    path = os.path.join("config", "fallback_config.json")
    if not os.path.exists(path):
        return {"error": "Missing fallback_config.json"}
    with open(path, "r") as f:
        return json.load(f)

@router.post("/fallback/update")
def update_fallback_config(payload: dict):
    os.makedirs("config", exist_ok=True)
    with open("config/fallback_config.json", "w") as f:
        json.dump(payload, f, indent=2)
    return {"message": "Fallback config updated"}
