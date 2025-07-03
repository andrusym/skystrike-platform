from fastapi import APIRouter

router = APIRouter(prefix="/bots", tags=["bots"])

# This should eventually pull from real status logic or a config file
@router.get("/{bot_name}/status")
async def get_bot_status(bot_name: str):
    """
    Return the current status for the given bot (placeholder logic).
    """
    # Replace this with actual fetch logic or config query
    status = "active" if bot_name in ["ironcondor", "kingcondor"] else "disabled"
    return {"bot_name": bot_name, "status": status}
