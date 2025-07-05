# backend/routes/journal_enhancer.py

import datetime
from backend.utils.database import save_journal_entry  # ? Fixed import

class JournalEnhancer:
    def __init__(self, user_id):
        self.user_id = user_id

    def log(self, trade_id, notes, tags=None):
        if tags is None:
            tags = []

        entry = {
            "user_id": self.user_id,
            "trade_id": trade_id,
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "notes": notes,
            "tags": tags
        }
        save_journal_entry(entry)
        return entry
