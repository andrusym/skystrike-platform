# backend/config.py
import os
from dotenv import load_dotenv

load_dotenv()  # <–– loads .env from your project root

class Settings:
    APP_ENV     = os.getenv("APP_ENV", "production")
    LOG_LEVEL   = os.getenv("LOG_LEVEL", "info")
    TRADE_MODE  = os.getenv("TRADIER_MODE", "paper").lower()

    if TRADE_MODE == "paper":
        TRADIER_API_KEY   = os.getenv("TRADIER_PAPER_ACCESS_TOKEN")
        TRADIER_ACCOUNT_ID = os.getenv("TRADIER_PAPER_ACCOUNT_ID")
    elif TRADE_MODE == "live":
        TRADIER_API_KEY   = os.getenv("TRADIER_LIVE_ACCESS_TOKEN")
        TRADIER_ACCOUNT_ID = os.getenv("TRADIER_LIVE_ACCOUNT_ID")
    else:
        raise RuntimeError(f"Invalid TRADE_MODE: {TRADE_MODE!r}")

# instantiate at module-level so it's only read once
settings = Settings()
