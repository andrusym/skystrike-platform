# backend/engine/bot_entry_engine.py

from backend.utils.fallback_manager import is_fallback_active
from backend.bots.iron_condor import run as run_ironcondor
from backend.bots.kingcondor import run as run_kingcondor
from backend.bots.wheel import run as run_wheel
from backend.bots.csp import run as run_csp
from backend.bots.trend import run as run_trend
from backend.bots.spread import run as run_spread
from backend.bots.replicator import run as run_replicator
from backend.bots.gridbot import run as run_gridbot
from backend.bots.dcabot import run as run_dcabot
from backend.bots.scalper import run as run_scalper
from backend.bots.pairstrader import run as run_pairstrader
from backend.bots.momentumbot import run as run_momentumbot
from backend.bots.copybot import run as run_copybot

bot_map = {
    "ironcondor": run_ironcondor,
    "kingcondor": run_kingcondor,
    "wheel": run_wheel,
    "csp": run_csp,
    "trend": run_trend,
    "spread": run_spread,
    "replicator": run_replicator,
    "gridbot": run_gridbot,
    "dcabot": run_dcabot,
    "scalper": run_scalper,
    "pairstrader": run_pairstrader,
    "momentumbot": run_momentumbot,
    "copybot": run_copybot,
}

def run_all_bots():
    if is_fallback_active():
        print("⚠️  [Fallback Active] Skipping all bot entries.")
        return

    print("🚀 Running all active bots...\n")
    for name, bot_func in bot_map.items():
        try:
            print(f"▶️  Executing {name}...")
            bot_func()
            print(f"✅  {name} completed successfully.\n")
        except Exception as e:
            print(f"❌ Error running {name}: {e}\n")

def execute_bot(name: str, ticker: str = None, contracts: int = 1, context: list = None):
    """
    Allows dynamic execution of a specific bot by name with params.
    """
    if name not in bot_map:
        raise ValueError(f"Bot '{name}' not recognized.")

    try:
        print(f"▶️ Triggering bot '{name}' via API with ticker={ticker}, contracts={contracts}")
        return bot_map[name](ticker=ticker, contracts=contracts, context=context or [])
    except Exception as e:
        print(f"❌ Error executing bot '{name}': {e}")
        raise
