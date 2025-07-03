import os
import json
from datetime import datetime
from backend.ml.ml_engine import load_ml_scores
from backend.engine.submit_order import run_bot_with_params

def send_orders_if_confident():
    ml_scores = load_ml_scores()
    for bot, info in ml_scores.items():
        if info["confidence"] >= 0.75:
            print(f"🚀 Submitting trade for {bot} with confidence {info['confidence']}")
            run_bot_with_params(bot=bot, ticker="SPX", contracts=1, dte=0)

if __name__ == "__main__":
    send_orders_if_confident()
