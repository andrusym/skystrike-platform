
class SpreadStrategy:
    def __init__(self, ticker: str):
        self.ticker = ticker

    def build_spread(self, expiration, width):
        chain = get_chain(self.ticker, expiration)
        mid = chain[len(chain)//2]['strike']
        lower = next(o for o in chain if o['strike'] == mid - width/2)
        upper = next(o for o in chain if o['strike'] == mid + width/2)
        return {
            "short_leg": lower['symbol'],
            "long_leg":  upper['symbol'],
            "quantity":  1
        }
