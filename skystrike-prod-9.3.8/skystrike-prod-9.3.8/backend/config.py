
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_ENV = os.getenv("APP_ENV", "development")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "debug")
    TRADIER_API_KEY = os.getenv("TRADIER_API_KEY")
    TRADIER_ACCOUNT_ID = os.getenv("TRADIER_ACCOUNT_ID")
    TRADE_MODE = os.getenv("TRADE_MODE", "paper")
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(",")

settings = Settings()
