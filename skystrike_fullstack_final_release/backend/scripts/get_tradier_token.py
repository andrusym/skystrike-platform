# backend/scripts/get_tradier_token.py

import os
import requests
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Determine mode (live or sandbox)
    raise ValueError("TRADIER_MODE must be either 'live' or 'sandbox'")

# Set credentials and token URL based on mode
    CLIENT_SECRET = os.getenv("TRADIER_LIVE_CLIENT_SECRET")
    TOKEN_URL = "https://api.tradier.com/v1/oauth/token"
else:
    CLIENT_ID = os.getenv("TRADIER_SANDBOX_CLIENT_ID")
    CLIENT_SECRET = os.getenv("TRADIER_SANDBOX_CLIENT_SECRET")
    TOKEN_URL = "https://sandbox.tradier.com/v1/oauth/token"

def get_tradier_token():
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "market"
    }

    response = requests.post(TOKEN_URL, headers=headers, data=data)
    if response.status_code == 200:
        token = response.json().get("access_token")
        print(f"\n? TRADIER_TOKEN:\n{token}\n")
        print(f"To use it in your session:\nexport TRADIER_TOKEN={token}\n")
    else:
        print("? Failed to retrieve token:")
        print(response.status_code, response.text)

if __name__ == "__main__":
    get_tradier_token()
