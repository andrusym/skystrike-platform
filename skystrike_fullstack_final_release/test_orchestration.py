import asyncio
from backend.engine.bot_entry_engine import run_all_bots

async def main():
    print("▶️  Running full orchestration…")
    results = await run_all_bots()
    print("\n✅ Results:")
    for bot, outcome in results.items():
        status = "OK" if outcome.get("success") else "FAIL"
        detail = outcome.get("payload") or outcome.get("error")
        print(f"  {status:4}  {bot:15}  {detail}")
        
if __name__ == "__main__":
    asyncio.run(main())
