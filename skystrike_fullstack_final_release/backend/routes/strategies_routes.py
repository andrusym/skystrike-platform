from fastapi import APIRouter
from fastapi.responses import JSONResponse
services.sync_bot_metadata import sync_bot_metadata

router = APIRouter()

@router.post("/trigger/{bot_name}")
def run_bot(bot_name: str):
    try:
        # PLACEHOLDER: your actual bot logic goes here
        print(f"Running bot: {bot_name}")

        # After running, sync metadata
        sync_result = sync_bot_metadata()
        return {"message": f"Bot {bot_name} triggered successfully", "sync": sync_result}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})