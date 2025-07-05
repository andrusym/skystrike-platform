def run_backtest(strategy, data):
    # Simplified sample backtest engine
    results = {"trades": [], "profit": 0}
    for i, entry in enumerate(data):
        signal = strategy(entry)
        if signal == "BUY":
            results["trades"].append({"index": i, "action": "BUY"})
        elif signal == "SELL":
            results["trades"].append({"index": i, "action": "SELL"})
    results["profit"] = len(results["trades"]) * 50  # dummy PnL
    return results