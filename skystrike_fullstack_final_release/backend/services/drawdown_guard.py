from datetime import datetime

def get_drawdown_status():
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "drawdown_limit": -0.15,
        "current_drawdown": -0.07,
        "protection_triggered": False,
        "note": "Simulated drawdown status — replace with real portfolio P&L tracking."
    }
