# backend/admin/audit_logger.py

import os
from datetime import datetime

LAST_RESTART_FILE = os.getenv(
    "LAST_RESTART_FILE",
    "/var/run/skystrike_last_restart.txt"
)

def get_last_restart() -> str:
    """
    Reads the timestamp of the last restart from disk.
    """
    if os.path.exists(LAST_RESTART_FILE):
        with open(LAST_RESTART_FILE, "r") as f:
            return f.read().strip()
    # Fallback to now if missing
    return datetime.utcnow().isoformat()
