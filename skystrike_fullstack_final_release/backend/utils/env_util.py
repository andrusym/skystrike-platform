# backend/utils/env_util.py

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

def get_token_and_account(mode: str = "paper") -> tuple[str, str]:
    """
    Returns (access_token, account_id) for the given mode.
    Mode must be either 'paper' or 'live'.
    """
    mode = mode.lower()

    if mode not in ["paper", "live"]:
        raise ValueError("Mode must be 'paper' or 'live'")

    access_token = os.getenv(f"TRADIER_{mode.upper()}_ACCESS_TOKEN")
    account_id   = os.getenv(f"TRADIER_{mode.upper()}_ACCOUNT_ID")

    if not access_token or not account_id:
        raise ValueError(f"Missing credentials for mode: {mode}")

    return access_token, account_id
