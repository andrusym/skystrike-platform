from fastapi import APIRouter, Request

router = APIRouter()

# Simulated trade replication endpoint
@router.post("/api/replicate-trade")
def replicate_trade(req: Request):
    payload = req.json()
    source_ticker = payload.get("source")
    targets = payload.get("targets", [])
    contracts = payload.get("contracts", 1)

    replicated = []
    for tgt in targets:
        replicated.append({
            "ticker": tgt,
            "action": "replicated",
            "contracts": contracts
        })

    return {"status": "success", "replicated": replicated}
