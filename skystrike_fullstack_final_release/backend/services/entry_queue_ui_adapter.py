
# entry_queue_ui_adapter.py

utils.database import get_upcoming_trades

def format_entry_queue():
    queue = get_upcoming_trades()
    formatted = [
        {
            "ticker": q["ticker"],
            "strategy": q["strategy"],
            "confidence": round(q["ml_score"], 2),
            "status": q["status"]
        }
        for q in queue
    ]
    return formatted
