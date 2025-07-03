import json
import os

def load_ml_scores(path="backend/ml/ml_scores.json"):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)
