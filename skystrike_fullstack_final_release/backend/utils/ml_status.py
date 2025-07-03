# backend/utils/ml_status.py

def get_ml_status():
    # Simulated static ML engine status
    return {
        "status": "online",
        "minScore": 0.6,
        "cooldownActive": False,
        "fallbacksTriggered": 3
    }
