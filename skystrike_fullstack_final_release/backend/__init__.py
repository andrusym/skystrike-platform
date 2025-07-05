import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        self.APP_ENV: str = os.getenv("APP_ENV", "production")
        self.LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")

        # Use 'sandbox' or 'live' only
        self.TRADE_MODE: str = os.getenv("TRADIER_MODE", "sandbox").lower()
        if self.TRADE_MODE not in ("sandbox", "live"):
            raise ValueError(f"? Invalid TRADIER_MODE: {self.TRADE_MODE}")

        # Load all credentials
        self.TRADIER_SANDBOX_ACCESS_TOKEN = os.getenv("TRADIER_SANDBOX_ACCESS_TOKEN")
        self.TRADIER_SANDBOX_ACCOUNT_ID = os.getenv("TRADIER_SANDBOX_ACCOUNT_ID")
        self.TRADIER_LIVE_ACCESS_TOKEN = os.getenv("TRADIER_LIVE_ACCESS_TOKEN")
        self.TRADIER_LIVE_ACCOUNT_ID = os.getenv("TRADIER_LIVE_ACCOUNT_ID")

        # Assign current credentials
        if self.TRADE_MODE == "sandbox":
            self.TRADIER_API_KEY = self.TRADIER_SANDBOX_ACCESS_TOKEN
            self.TRADIER_ACCOUNT_ID = self.TRADIER_SANDBOX_ACCOUNT_ID
        else:
            self.TRADIER_API_KEY = self.TRADIER_LIVE_ACCESS_TOKEN
            self.TRADIER_ACCOUNT_ID = self.TRADIER_LIVE_ACCOUNT_ID

        if not self.TRADIER_API_KEY or not self.TRADIER_ACCOUNT_ID:
            raise ValueError(f"? Missing Tradier credentials for mode: {self.TRADE_MODE}")

        # Optional CORS
        self.ALLOWED_ORIGINS: list[str] = os.getenv("ALLOWED_ORIGINS", "*").split(",")

        # JWT
        self.SECRET_KEY = os.getenv("JWT_SECRET", "changeme123")
        self.ALGORITHM = os.getenv("ALGORITHM", "HS256")
        self.ACCESS_TOKEN_EXPIRE_HOURS = int(os.getenv("ACCESS_TOKEN_EXPIRE_HOURS", 12))

        # Config paths
        self.BOT_CONFIG_PATH = os.getenv("BOT_CONFIG_PATH", "config/bot_config.json")
        self.CONTRACT_LIMITS_PATH = os.getenv("CONTRACT_LIMITS_PATH", "config/contract_limits.json")
        self.PORTFOLIO_GOALS_PATH = os.getenv("PORTFOLIO_GOALS_PATH", "config/portfolio_profiles.json")

    def tradier_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.TRADIER_API_KEY}",
            "Accept": "application/json"
        }

# ? Global instance
settings = Settings()
