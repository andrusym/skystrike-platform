# correlation_monitor.py
def check_conflicts(active_tickers):
    overlap = set()
    index_map = {
        "SPX": "SPX",
        "NDX": "QQQ",
        "QQQ": "QQQ",
        "XSP": "SPX",
        "DIA": "DIA"
    }
    groups = {}
    for t in active_tickers:
        base = index_map.get(t, t)
        groups.setdefault(base, []).append(t)

    for tickers in groups.values():
        if len(tickers) > 1:
            overlap.update(tickers)

    return list(overlap)
