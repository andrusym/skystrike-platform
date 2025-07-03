# strategy_lifecycle.py
def should_retire(hit_rate):
    return hit_rate < 40

def should_reactivate(hit_rate):
    return hit_rate > 60
