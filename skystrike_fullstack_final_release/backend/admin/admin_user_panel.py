# backend/admin/admin_user_panel.py

import os
import json

USERS_FILE = os.getenv("USERS_FILE", "data/users.json")

def get_all_users():
    """
    Reads users from a JSON file on disk.
    """
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def add_user(username: str, role: str = "user"):
    """
    Appends a new user; writes back to disk.
    """
    users = get_all_users()
    new = {"username": username, "role": role, "created": datetime.utcnow().isoformat()}
    users.append(new)
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)
    return new
