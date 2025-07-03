# backend/config/load_config.py

import json
import os

CONFIG_PATH = "backend/config/bot_config.json"

def load_bot_config():
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(f"Missing config file: {CONFIG_PATH}")
    
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)
