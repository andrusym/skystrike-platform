"""
Handles multi-user authentication, roles, and permissions.
"""
class User:
    def __init__(self, username, role='trader'):
        self.username = username
        self.role = role

    def has_permission(self, action):
        role_permissions = {
            "admin": {"view", "trade", "config"},
            "trader": {"view", "trade"},
            "viewer": {"view"}
        }
        return action in role_permissions.get(self.role, set())
