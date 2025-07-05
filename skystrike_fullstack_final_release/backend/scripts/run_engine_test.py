import sys
import asyncio

# Add the engines directory to the import path
sys.path.append("./engines")

from trading_engine import run_smart_trading_engines

asyncio.run(run_smart_trading_engines())
