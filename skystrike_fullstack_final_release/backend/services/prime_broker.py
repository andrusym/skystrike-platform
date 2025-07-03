"""
Route trades to appropriate prime broker endpoints.
"""
class PrimeBrokerRouter:
    def __init__(self):
        self.routes = {"default": "tradier", "institutional": "prime_broker"}

    def route_order(self, account_type):
        return self.routes.get(account_type, self.routes["default"])
