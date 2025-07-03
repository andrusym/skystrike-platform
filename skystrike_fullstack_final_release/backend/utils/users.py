import json
import bcrypt
from datetime import datetime

USERS_FILE = "data/users.json"

def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def create_user(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = {
        "password_hash": hash_password(password),
        "goal": "balanced",
        "account_size": 10000,
        "tradier_token": "",
        "tradier_mode": "paper",
        "last_login": datetime.utcnow().isoformat()
    }
    save_users(users)
    return True

def get_user(username):
    return load_users().get(username)

def update_user(username, updates):
    users = load_users()
    if username in users:
        users[username].update(updates)
        save_users(users)
        return True
    return False
