from models.session import SessionLocal
from models.user_model import DBUser
utils.security import hash_password

db = SessionLocal()

admin_user = DBUser(
    username="admin",
    password_hash=hash_password("webflows3"),
    goal="balanced",
    account_size=25000,
    tradier_mode="paper"
)

try:
    db.add(admin_user)
    db.commit()
    print("[+] Admin user created.")
except Exception as e:
    db.rollback()
    print(f"[!] Failed to insert admin user: {e}")
finally:
    db.close()
