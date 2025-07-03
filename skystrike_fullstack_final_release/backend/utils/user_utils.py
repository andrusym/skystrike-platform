# utils/user_utils.py

import json
import os

USER_FILE = os.path.join(os.path.dirname(__file__), "../db/users.json")

def load_users():
    if not os.path.exists(USER_FILE):
        return []
    with open(USER_FILE, "r") as f:
        return json.load(f)
