import asyncio
from datetime import datetime, timedelta
services.tradier_api import place_order, get_quote

async def send_ironcondor_order(ticker="SPY", contracts=1):
    # Fetch latest quote
    quote = await get_quote(ticker)
    if not quote or "last" not in quote:
        print(f"Error: No quote data for {ticker}")
        return

    mid_price = float(quote["last"])
    width = 5.0  # strike width in dollars

    strikes = {
        "short_call": round(mid_price + width, 1),
        "long_call": round(mid_price + 2 * width, 1),
        "short_put": round(mid_price - width, 1),
        "long_put": round(mid_price - 2 * width, 1),
    }

    expiry_date = (datetime.utcnow() + timedelta(days=1)).date()

    def format_symbol(ticker, exp, cp, strike):
        exp_str = exp.strftime('%y%m%d')
        strike_fmt = f"{int(strike * 1000):08d}"
        return f"{ticker.upper()}{exp_str}{cp}{strike_fmt}"

    legs = [
        {"side": "sell_to_open", "option_symbol": format_symbol(ticker, expiry_date, "C", strikes["short_call"]), "quantity": contracts},
        {"side": "buy_to_open",  "option_symbol": format_symbol(ticker, expiry_date, "C", strikes["long_call"]),  "quantity": contracts},
        {"side": "sell_to_open", "option_symbol": format_symbol(ticker, expiry_date, "P", strikes["short_put"]),  "quantity": contracts},
        {"side": "buy_to_open",  "option_symbol": format_symbol(ticker, expiry_date, "P", strikes["long_put"]),   "quantity": contracts},
    ]

    order_payload = {
        "class": "multileg",
        "symbol": ticker,
        "type": "market",
        "duration": "day",
        "legs": legs
    }

    print("Sending order payload:")
    for k, v in order_payload.items():
        print(f"{k}: {v}")

    response = await place_order(order_payload)
    print("Tradier response:")
    print(response)

if __name__ == "__main__":
    asyncio.run(send_ironcondor_order())
