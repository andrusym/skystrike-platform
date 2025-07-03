import os
import httpx
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TRADIER_PAPER_ACCESS_TOKEN")
BASE_URL = "https://sandbox.tradier.com/v1"

if not TOKEN:
    print("No TRADIER_PAPER_ACCESS_TOKEN found in .env")
    exit(1)

async def test_token():
    url = f"{BASE_URL}/user/profile"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/json",
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        print(response.status_code)
        print(response.text)

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_token())
