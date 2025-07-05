
# Cash Secured Put Strategy
def run_csp(symbol: str, capital: float):
    strike_price = round(capital * 0.95)  # simplistic strike targeting
    return {
        "strategy": "CSP",
        "symbol": symbol,
        "action": "Sell Put Option",
        "strike": strike_price,
        "capital_used": capital
    }
