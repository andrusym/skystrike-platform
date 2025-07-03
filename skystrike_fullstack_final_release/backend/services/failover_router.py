"""
Handles broker failover routing to ensure order placement continuity.
"""
class FailoverRouter:
    def __init__(self, primary, backup):
        self.primary = primary
        self.backup = backup

    def route_order(self, *args, **kwargs):
        try:
            return self.primary(*args, **kwargs)
        except Exception:
            return self.backup(*args, **kwargs)
