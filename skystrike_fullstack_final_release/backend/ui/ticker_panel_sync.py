
# ticker_panel_sync.py

utils.database import get_live_pnl_by_ticker, get_strategy_count

def build_ticker_panel(tickers):
    panel = []
    for t in tickers:
        pnl = get_live_pnl_by_ticker(t)
        strategies = get_strategy_count(t)
        panel.append({
            "ticker": t,
            "pnl": pnl,
            "strategies_active": strategies
        })
    return panel
