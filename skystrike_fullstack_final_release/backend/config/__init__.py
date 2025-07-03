import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_ENV: str = os.getenv("APP_ENV", "production")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")
    TRADE_MODE: str = os.getenv("TRADIER_MODE", "paper").lower()

    if TRADE_MODE == "paper":
        TRADIER_API_KEY: str = os.getenv("TRADIER_PAPER_ACCESS_TOKEN")
        TRADIER_ACCOUNT_ID: str = os.getenv("TRADIER_PAPER_ACCOUNT_ID")
    elif TRADE_MODE == "live":
        TRADIER_API_KEY: str = os.getenv("TRADIER_LIVE_ACCESS_TOKEN")
        TRADIER_ACCOUNT_ID: str = os.getenv("TRADIER_LIVE_ACCOUNT_ID")
    else:
        raise ValueError(f"❌ Invalid TRADIER_MODE: {TRADE_MODE}")

    ALLOWED_ORIGINS: list[str] = os.getenv("ALLOWED_ORIGINS", "*").split(",")

    def tradier_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.TRADIER_API_KEY}",
            "Accept": "application/json"
        }

# ✅ This line is required
settings = Settings()
