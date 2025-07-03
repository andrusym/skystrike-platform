#!/usr/bin/env bash
set -euo pipefail

bots=(iron_condor kingcondor spread csp wheel trend replicator \
      copybot dcabot gridbot momentumbot pair_trading_engine pairstrader scalper)

echo "Testing build_order_for_bot for each strategy..."
for b in "${bots[@]}"; do
  echo; echo "=== $b ==="
  python3 - <<PYCODE
import json
from backend.services.order_builder import build_order_for_bot
try:
    form = build_order_for_bot("$b", "SPY", contracts=1, confidence=0.85)
    print(json.dumps(form, indent=2))
except Exception as e:
    print("ERROR:", e)
PYCODE
done
