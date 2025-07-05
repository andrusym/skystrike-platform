from typing import Dict, Any

from backend.services.dynamic_dte_selector import get_vix_level
from backend.bots.iron_condor import build_order as build_condor
from backend.bots.trend import build_order as build_trend

def build_order(
    ticker: str = "SPX",
    contracts: int = 1,
    dte: int = None,
    mode: str = None,
    confidence: float = None
) -> Dict[str, Any]:
    vix = get_vix_level()
    if vix is None:
        raise RuntimeError("VIX level unavailable")

    if vix >= 20:
        strategy = "iron_condor"
        order = build_condor(
            ticker=ticker,
            contracts=contracts,
            dte=dte,
            mode=mode,
            confidence=confidence
        )
    else:
        strategy = "trend"
        order = build_trend(
            ticker=ticker,
            contracts=contracts,
            dte=dte,
            mode=mode,
            confidence=confidence
        )

    # annotate metadata
    order.setdefault("metadata", {})
    order["metadata"].update({
        "bot": "hybrid_bot",
        "strategy_used": strategy,
        "vix": vix
    })
    return order
