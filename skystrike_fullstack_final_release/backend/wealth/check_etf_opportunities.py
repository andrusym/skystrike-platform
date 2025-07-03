import random
from datetime import datetime

# Sample ETF list — you can expand or pull from config
ETF_LIST = ["VTI", "SCHD", "JEPI", "QQQ", "SPY", "ARKK"]

def evaluate_etfs():
    """
    Simulate ETF dip-buying opportunities or scoring logic.
    Replace this with actual price/indicator analysis later.
    """
    opportunities = {}
    for etf in ETF_LIST:
        opportunities[etf] = {
            "score": round(random.uniform(0.5, 0.95), 2),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "signal": "buy" if random.random() > 0.4 else "hold"
        }
    return opportunities
