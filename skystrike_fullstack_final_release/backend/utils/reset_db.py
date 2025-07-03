# backend/scripts/reset_db.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

db.models import Base
db.session import engine

def reset_database():
    print("[*] Dropping and recreating all tables ...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("[*] Done.")

if __name__ == "__main__":
    reset_database()
