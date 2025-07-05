import os
from dotenv import load_dotenv

load_dotenv()  # loads from project root/backend/.env (if present)

class Settings:
    # core app settings
    APP_ENV = os.getenv("APP_ENV", "production")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "info")

    # trading mode: "sandbox" or "live"
    TRADE_MODE = os.getenv("TRADIER_MODE", "sandbox").lower()
    if TRADE_MODE not in ("sandbox", "live"):
        raise RuntimeError(f"Invalid TRADIER_MODE: {TRADE_MODE!r}")

    # pick Tradier creds by mode
    if TRADE_MODE == "sandbox":
        TRADIER_ACCESS_TOKEN = os.getenv("TRADIER_SANDBOX_ACCESS_TOKEN")
        TRADIER_ACCOUNT_ID   = os.getenv("TRADIER_SANDBOX_ACCOUNT_ID")
    else:
        TRADIER_ACCESS_TOKEN = os.getenv("TRADIER_LIVE_ACCESS_TOKEN")
        TRADIER_ACCOUNT_ID   = os.getenv("TRADIER_LIVE_ACCOUNT_ID")

    if not TRADIER_ACCESS_TOKEN or not TRADIER_ACCOUNT_ID:
        raise RuntimeError(f"Missing Tradier credentials for mode {TRADE_MODE!r}")

    # JWT / auth
    SECRET_KEY                = os.getenv("SECRET_KEY")
    ALGORITHM                 = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

    # CORS
    ALLOWED_ORIGINS = [
        origin.strip()
        for origin in os.getenv("ALLOWED_ORIGINS", "").split(",")
        if origin.strip()
    ]

settings = Settings()
