# backend/services/rounding_util.py

import math
from typing import List

def round_price(price: float, precision: int = 2) -> float:
    """
    Round a float price to the given number of decimal places.
    """
    return round(price, precision)

def round_to_increment(value: float, increment: float) -> float:
    """
    Round 'value' to the nearest multiple of 'increment'.
    E.g. round_to_increment(101.3, 0.5) ? 101.5
    """
    return round(value / increment) * increment

def floor_to_increment(value: float, increment: float) -> float:
    """
    Round 'value' down to the nearest multiple of 'increment'.
    E.g. floor_to_increment(101.3, 0.5) ? 101.0
    """
    return math.floor(value / increment) * increment

def ceil_to_increment(value: float, increment: float) -> float:
    """
    Round 'value' up to the nearest multiple of 'increment'.
    E.g. ceil_to_increment(101.1, 0.5) ? 101.5
    """
    return math.ceil(value / increment) * increment

def get_nearest_strike(available_strikes: List[float], target: float) -> float:
    """
    From a list of strike prices, pick the one closest to 'target'.
    """
    return min(available_strikes, key=lambda s: abs(s - target))
