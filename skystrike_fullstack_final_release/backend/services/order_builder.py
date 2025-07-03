# backend/order_builder_registry.py

from backend.bots.iron_condor import build_order as ic_build
from backend.bots.kingcondor import build_order as kc_build
from backend.bots.spread import build_order as spread_build
from backend.bots.csp import build_order as csp_build
from backend.bots.wheel import build_order as wheel_build
from backend.bots.trend import build_order as trend_build
from backend.bots.replicator import build_order as rep_build
from backend.bots.copybot import build_order as copy_build
from backend.bots.dcabot import build_order as dca_build
from backend.bots.gridbot import build_order as grid_build
from backend.bots.momentumbot import build_order as momentum_build
from backend.bots.scalper import build_order as scalp_build
from backend.bots.pairstrader import build_order as pair_build

# Optional: if adding new bots, import here and append to BUILD_MAP
# e.g., from backend.bots.squeeze import build_order as squeeze_build

BUILD_MAP = {
    "ironcondor": ic_build,
    "kingcondor": kc_build,
    "spread": spread_build,
    "csp": csp_build,
    "wheel": wheel_build,
    "trend": trend_build,
    "replicator": rep_build,
    "copybot": copy_build,
    "dcabot": dca_build,
    "gridbot": grid_build,
    "momentumbot": momentum_build,
    "scalper": scalp_build,
    "pairstrader": pair_build,
    # "squeeze": squeeze_build,  # Uncomment when implemented
}


def get_order_builder(bot_name: str):
    """Safely retrieve the build_order function for the given bot."""
    builder = BUILD_MAP.get(bot_name.lower())
    if not builder:
        raise ValueError(f"Unsupported bot name: '{bot_name}'")
    return builder
