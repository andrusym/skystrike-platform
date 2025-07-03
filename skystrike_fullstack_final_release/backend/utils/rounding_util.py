
def round_strike_to_valid_increment(ticker: str, strike: float) -> float:
    """
    Rounds the strike price to the nearest valid Tradier-supported increment.
    """
    ticker = ticker.upper()
    if ticker in {"SPY", "QQQ", "NDX", "SPX", "XSP"}:
        increment = 1.0
    elif ticker in {"IWM", "AAPL", "TSLA"}:
        increment = 0.5
    else:
        increment = 1.0
    return round(strike / increment) * increment
