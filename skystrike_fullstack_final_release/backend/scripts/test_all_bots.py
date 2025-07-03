#!/usr/bin/env python3
import os
import asyncio
from backend.submit_order import run_bot_with_params, BUILD_MAP

async def main():
    # default to paper mode if not set
    os.environ.setdefault("TRADIER_MODE", "paper")

    bots = sorted(BUILD_MAP.keys())
    successes = []
    failures = []

    for bot in bots:
        print(f"--- Testing {bot} ---")
        result = await run_bot_with_params(
            bot=bot,
            ticker="SPY",
            contracts=1,
            dte=1,
            mode="paper"
        )
        if result.get("status") == "success":
            print("? Success:", result["response"])
            successes.append(bot)
        else:
            print("?? Failure:", result.get("error") or result)
            failures.append((bot, result))

    print(f"\nSummary: {len(successes)} succeeded, {len(failures)} failed.")
    if failures:
        print("Failed bots:")
        for bot, res in failures:
            print(f" - {bot}: {res}")
        # exit with error so CI/test harness knows something broke
        exit(1)

if __name__ == "__main__":
    asyncio.run(main())
