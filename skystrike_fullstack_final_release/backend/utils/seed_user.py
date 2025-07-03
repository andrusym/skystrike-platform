# backend/scripts/seed_user.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

db.models import User
db.session import SessionLocal
utils.auth import hash_password

def seed_admin():
    db = SessionLocal()
    user = User(
        username="admin",
        password_hash=hash_password("webflows3"),
        goal="balanced",
        account_size=25000,
        tradier_mode="paper"
    )
    db.add(user)
    try:
        db.commit()
        print("[+] Admin user created.")
    except Exception as e:
        db.rollback()
        print("[!] Error seeding user:", e)
    finally:
        db.close()

if __name__ == "__main__":
    seed_admin()
