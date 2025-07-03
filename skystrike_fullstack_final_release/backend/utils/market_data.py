import requests

TRADIER_API_URL = "https://api.tradier.com/v1/markets/quotes"
TRADIER_HEADERS = {
    "Authorization": "Bearer YOUR_TRADIER_TOKEN",
    "Accept": "application/json"
}

def fetch_market_quotes(symbols=["SPY", "^VIX"]):
    try:
        response = requests.get(
            TRADIER_API_URL,
            headers=TRADIER_HEADERS,
            params={"symbols": ",".join(symbols)}
        )
        if response.status_code == 200:
            data = response.json().get("quotes", {}).get("quote", [])
            quotes = {q["symbol"]: q["last"] for q in (data if isinstance(data, list) else [data])}
            return quotes
        else:
            print("Tradier API Error:", response.status_code, response.text)
            return {}
    except Exception as e:
        print("Error fetching quotes:", e)
        return {}
