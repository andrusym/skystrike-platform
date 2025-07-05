import yfinance as yf
from datetime import datetime, timedelta
import json

def run_backtest(ticker="SPY", strategy="ironcondor", days=30):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=days)

    df = yf.download(ticker, start=start_date, end=end_date)
    if df.empty:
        return {"error": "No data for backtest"}

    simulated_trades = []
    for i in range(5, len(df)-5, 5):  # simulate every 5 days
        entry_price = df.iloc[i]["Close"]
        exit_price = df.iloc[i+5]["Close"]
        pnl = simulate_strategy(strategy, entry_price, exit_price)

        simulated_trades.append({
            "bot": strategy,
            "symbol": ticker,
            "entry": str(df.index[i].date()),
            "exit": str(df.index[i+5].date()),
            "pnl": round(pnl, 2)
        })

    return simulated_trades

def simulate_strategy(strategy, entry_price, exit_price):
    if strategy in ["ironcondor", "kingcondor"]:
        return 50 if abs(exit_price - entry_price) < 2 else -100
    if strategy == "trend":
        return 100 if exit_price > entry_price else -100
    if strategy == "wheel":
        return 40 if exit_price >= entry_price else -50
    return 0