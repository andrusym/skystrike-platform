# backend/schedulers/config_backup_logger.py

import os
import json
from datetime import datetime

CONFIG_PATH = "backend/config/bot_config.json"
BACKUP_DIR = "logs/config_backups"
LOG_FILE = "logs/config_change_log.json"

os.makedirs(BACKUP_DIR, exist_ok=True)

timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
backup_path = os.path.join(BACKUP_DIR, f"bot_config_{timestamp}.json")

try:
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)

    # Save snapshot
    with open(backup_path, "w") as f:
        json.dump(config, f, indent=2)

    # Append timestamp to audit log
    log_entry = {
        "timestamp": timestamp,
        "backup_file": backup_path
    }

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            log_data = json.load(f)
    else:
        log_data = []

    log_data.append(log_entry)

    with open(LOG_FILE, "w") as f:
        json.dump(log_data, f, indent=2)

    print(f"✅ Backed up config to {backup_path}")

except Exception as e:
    print(f"❌ Backup failed: {e}")
