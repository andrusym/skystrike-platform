import json
from datetime import datetime
from sklearn.neighbors import NearestNeighbors
import numpy as np

INPUT_FILE = "ml/historical_trades.json"

def vectorize(trade):
    return np.array([
        float(trade.get("entry_price", 0)),
        int(trade.get("dte", 0)),
        float(trade.get("iv", 0)),
        int(trade.get("hour", 12))
    ])

def score_trade_against_history(new_trade):
    with open(INPUT_FILE) as f:
        past_trades = json.load(f)

    relevant = [t for t in past_trades if t["strategy"] == new_trade["strategy"]]
    if not relevant:
        return 0.5  # fallback

    X = np.array([vectorize(t) for t in relevant])
    y = np.array([1 if t["pnl"] > 0 else 0 for t in relevant])

    model = NearestNeighbors(n_neighbors=min(5, len(X)))
    model.fit(X)

    _, indices = model.kneighbors([vectorize(new_trade)])
    return y[indices[0]].mean()
