
# journal_enhancer.py

import datetime
utils.database import save_journal_entry

class JournalEnhancer:
    def __init__(self, user_id):
        self.user_id = user_id

    def log(self, trade_id, notes, tags=[]):
        entry = {
            "user_id": self.user_id,
            "trade_id": trade_id,
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "notes": notes,
            "tags": tags
        }
        save_journal_entry(entry)
        return entry
