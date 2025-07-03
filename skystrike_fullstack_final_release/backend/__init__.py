import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        self.APP_ENV: str = os.getenv("APP_ENV", "production")
        self.LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")
        self.TRADE_MODE: str = os.getenv("TRADIER_MODE", "paper").lower()

        # Load both paper and live credentials explicitly
        self.TRADIER_PAPER_ACCESS_TOKEN: str = os.getenv("TRADIER_PAPER_ACCESS_TOKEN")
        self.TRADIER_PAPER_ACCOUNT_ID: str = os.getenv("TRADIER_PAPER_ACCOUNT_ID")
        self.TRADIER_LIVE_ACCESS_TOKEN: str = os.getenv("TRADIER_LIVE_ACCESS_TOKEN")
        self.TRADIER_LIVE_ACCOUNT_ID: str = os.getenv("TRADIER_LIVE_ACCOUNT_ID")

        # Set active credentials based on mode
        if self.TRADE_MODE == "paper":
            self.TRADIER_API_KEY = self.TRADIER_PAPER_ACCESS_TOKEN
            self.TRADIER_ACCOUNT_ID = self.TRADIER_PAPER_ACCOUNT_ID
        elif self.TRADE_MODE == "live":
            self.TRADIER_API_KEY = self.TRADIER_LIVE_ACCESS_TOKEN
            self.TRADIER_ACCOUNT_ID = self.TRADIER_LIVE_ACCOUNT_ID
        else:
            raise ValueError(f"? Invalid TRADIER_MODE: {self.TRADE_MODE}")

        # Optional CORS
        self.ALLOWED_ORIGINS: list[str] = os.getenv("ALLOWED_ORIGINS", "*").split(",")

    def tradier_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.TRADIER_API_KEY}",
            "Accept": "application/json"
        }

# ? Expose instance
settings = Settings()
