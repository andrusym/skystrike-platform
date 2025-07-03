# backend/services/strike_picker.py
import httpx
from typing import List

class StrikePicker:
    def __init__(self, endpoint: str):
        self.client = httpx.AsyncClient(base_url=endpoint)

    async def pick_call_strikes(self, symbol: str, confidence: float) -> List[str]:
        resp = await self.client.post(
            "/v1/models/strikes:predict",
            json={"symbol": symbol, "confidence": confidence, "type": "call"},
        )
        resp.raise_for_status()
        return resp.json()["strikes"]

    async def pick_put_strikes(self, symbol: str, confidence: float) -> List[str]:
        resp = await self.client.post(
            "/v1/models/strikes:predict",
            json={"symbol": symbol, "confidence": confidence, "type": "put"},
        )
        resp.raise_for_status()
        return resp.json()["strikes"]
