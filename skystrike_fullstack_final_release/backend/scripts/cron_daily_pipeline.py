# backend/scripts/cron_daily_pipeline.py

import asyncio
from engine.system_orchestrator import full_daily_engine_run

async def main():
    print("? Cronjob: Running daily ML + tuning pipeline...")
    result = full_daily_engine_run()
    print("? Pipeline complete. Final recommendation:")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
