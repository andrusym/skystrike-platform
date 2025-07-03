# In-memory user store for simplicity
users_db = {
    "testuser": {"username": "testuser", "password": "testpass"}
}

def get_user_by_username(username: str):
    return users_db.get(username)