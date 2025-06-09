
import datetime
import random

def get_option_chain(ticker):
    strikes = [round(x, 1) for x in range(350, 451, 5)]
    chain = {
        "calls": {},
        "puts": {}
    }

    expiration_dates = [
        (datetime.date.today() + datetime.timedelta(days=3)).isoformat(),
        (datetime.date.today() + datetime.timedelta(days=10)).isoformat(),
        (datetime.date.today() + datetime.timedelta(days=17)).isoformat()
    ]

    for strike in strikes:
        for exp in expiration_dates:
            call_key = (strike, exp)
            put_key = (strike, exp)
            chain["calls"][call_key] = {
                "strike": strike,
                "expiration": exp,
                "bid": round(random.uniform(1.0, 3.5), 2),
                "ask": round(random.uniform(3.6, 6.0), 2),
                "volume": random.randint(100, 1000)
            }
            chain["puts"][put_key] = {
                "strike": strike,
                "expiration": exp,
                "bid": round(random.uniform(1.0, 3.5), 2),
                "ask": round(random.uniform(3.6, 6.0), 2),
                "volume": random.randint(100, 1000)
            }

    return chain
