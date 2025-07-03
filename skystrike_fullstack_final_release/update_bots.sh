#!/usr/bin/env bash
set -euo pipefail

ROOT="\$(pwd)"
SRV="\$ROOT/backend/services"

echo "Backing up and installing dynamic order_builder..."
cp "\$SRV/order_builder.py" "\$SRV/order_builder.py.bak"
cat > "\$SRV/order_builder.py" << 'PYCODE'
import importlib
from fastapi import HTTPException
from backend.services.tradier_api import calculate_expiration, get_option_chain

# default DTE per bot
DTE_DEFAULTS = {
    "iron_condor": 0, "kingcondor": 0,
    "spread": 1, "csp": 1, "wheel": 1, "trend": 1
}

def build_order_for_bot(bot_name: str, symbol: str, contracts: int = 1, confidence: float = 0.85) -> dict:
    module_name = bot_name.replace(" ", "_").lower()
    full_mod = f"backend.bots.{module_name}"
    try:
        mod = importlib.import_module(full_mod)
    except ModuleNotFoundError:
        raise HTTPException(status_code=404, detail=f"Bot not found: {module_name}")

    # calculate expiration
    dte = DTE_DEFAULTS.get(module_name, 1)
    expiration = calculate_expiration(dte)

    # if bot is options‐based, verify chain
    if getattr(mod, "OPTIONS_BASED", False):
        if not get_option_chain(symbol, expiration):
            raise HTTPException(status_code=502, detail=f"No chain for {symbol} exp={expiration}")

    # call the bot's build_order()
    try:
        form = mod.build_order(
            symbol=symbol,
            contracts=contracts,
            confidence=confidence,
            expiration=expiration
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{module_name}.build_order error: {e}")

    # defaults
    form.setdefault("symbol", symbol)
    form.setdefault("type",   "market")
    form.setdefault("duration","day")
    if "class" not in form:
        form["class"] = "multileg" if any(k.startswith("option_symbol") for k in form) else "option"

    return form
PYCODE

echo "Generating test_bots.sh..."
cat > test_bots.sh << 'SCRIPT'
#!/usr/bin/env bash
set -euo pipefail

bots=(iron_condor kingcondor spread csp wheel trend replicator \
      copybot dcabot gridbot momentumbot pairtradingengine pairstrader scalper)

echo "Testing build_order_for_bot for each strategy..."
for b in "${bots[@]}"; do
  echo; echo "=== \$b ==="
  python3 - <<PYCODE
import json
from backend.services.order_builder import build_order_for_bot
try:
    form = build_order_for_bot("\$b", "SPY", contracts=1)
    print(json.dumps(form, indent=2))
except Exception as e:
    print("ERROR:", e)
PYCODE
done
SCRIPT

echo "Restarting Uvicorn..."
pkill -f uvicorn || true
nohup uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload &>/dev/null &

echo "Running test_bots.sh..."
chmod +x test_bots.sh
./test_bots.sh

echo "Done."
