"""
Monitors API latency and execution delay for broker interactions.
"""
import time

class LatencyMonitor:
    def __init__(self):
        self.history = []

    def time_call(self, func, *args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        latency = time.time() - start
        self.history.append(latency)
        return result

    def get_average_latency(self):
        return sum(self.history) / len(self.history) if self.history else 0.0
