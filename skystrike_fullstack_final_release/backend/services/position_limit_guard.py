"""
Checks position sizing and prevents over-leveraging or breaching limits.
"""
class PositionLimitGuard:
    def __init__(self, max_position_per_symbol=100):
        self.max_position = max_position_per_symbol

    def is_within_limit(self, symbol, current_position, new_qty):
        return (current_position + new_qty) <= self.max_position
