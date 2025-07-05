# backend/scripts/cron_final_recommendation.py

import asyncio
from engine import generate_final_recommendation

async def main():
    print("? Cronjob: Running final portfolio recommendation...")
    result = generate_final_recommendation()
    print("? Final recommendation complete:")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
