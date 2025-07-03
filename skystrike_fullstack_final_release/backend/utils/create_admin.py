# scripts/create_admin.py
db.session import get_db
db.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db = next(get_db())

# Replace these with your defaults
username = "admin"
password = "admin123"
hashed = pwd_context.hash(password)

# Optional: wipe duplicates first
db.query(User).filter(User.username == username).delete()

# Create user
user = User(
    username=username,
    password_hash=hashed,
    goal="aggressive",
    account_size=100000,
    tradier_mode="paper"
)
db.add(user)
db.commit()
print("? Admin user created")
