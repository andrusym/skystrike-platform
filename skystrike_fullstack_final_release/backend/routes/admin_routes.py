# backend/routes/admin_routes.py

from fastapi import APIRouter, Header, HTTPException
from backend.admin.admin_user_panel import get_all_users
from backend.admin.admin_user_manager import get_user_stats
from backend.admin.audit_logger import get_last_restart

router = APIRouter()

@router.get("/admin/dashboard")
def render_admin_dashboard(auth: str = Header(None)):
    # TODO: verify the auth token here, e.g. using your verify_token function:
    # try:
    #     verify_token(auth)
    # except Exception:
    #     raise HTTPException(status_code=401, detail="Unauthorized")

    users = get_all_users()
    stats = get_user_stats()
    last_restart = get_last_restart()

    return {
        "status": "ok",
        "metrics": {
            "active_users": len(users),
            "queued_orders": stats.get("queued_orders", 0),
            "last_restart": last_restart,
        },
        "users": users
    }
