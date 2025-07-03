cat > ~/skystrike_fullstack_final_release/backend/cleanup.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail

# ** CORRECT path below **
cd /home/ubuntu/skystrike_fullstack_final_release/backend

echo "? 1. Remove root-level bot stubs & tests"
rm -f send_ironcondor_order.py bots.py bot_runner.py test_tradier_token.py

echo "? 2. Remove old strategies folder"
rm -rf strategies

echo "? 3. Prune duplicate bot routers"
rm -f routes/bot_trigger_dynamic.py routes/bots.py

echo "? 4. Create new bots package"
mkdir -p bots
cat > bots/__init__.py << 'EOI'
# Auto-generated registry of all live bots
BOT_RUNNERS = {
    # fill in after move
}
EOI

echo "? 5. Move every file that defines run_bot_with_params() into bots/"
find . -maxdepth 1 -type f -name "*.py" \
  -exec grep -Il "def run_bot_with_params" {} \; \
  | xargs -I{} bash -c 'mv "$1" "bots/$(basename "$1")"; echo "  • Moved $1 ? bots/$(basename "$1")"' _ {}

echo "? 6. Move any other named-strategy scripts"
if [ -d scripts ]; then
  find scripts -type f -name "*condor*.py" \
    | xargs -I{} bash -c 'mv "$1" "bots/$(basename "$1")"; echo "  • Moved $1 ? bots/$(basename "$1")"' _ {}
fi

echo "? 7. Create shared helper file"
mkdir -p utils
cat > utils/market_helpers.py << 'EOM'
import asyncio
from datetime import datetime, timedelta
import pytz
from services.tradier_api import get_quote

TZ = pytz.timezone("US/Eastern")
CLOSE_HOUR = 16

def is_expiry_day():
    return datetime.now(TZ).weekday() == 4

def is_before_close():
    now = datetime.now(TZ)
    return now.hour < CLOSE_HOUR

def get_next_expiry(dte=1):
    today = datetime.now(TZ)
    if dte == 0 and is_expiry_day() and is_before_close():
        return today.strftime("%Y-%m-%d")
    days = (4 - today.weekday()) % 7 or 7
    target = today + timedelta(days=(dte if dte>0 else days))
    while target.weekday() > 4:
        target += timedelta(days=1)
    return target.strftime("%Y-%m-%d")

def get_atm_strike(sym):
    data = asyncio.run(get_quote(sym))
    q = data.get("quotes",{}).get("quote",{})
    last = float(q["last"]) if isinstance(q,dict) else float(q[0]["last"])
    return int(round(last/5)*5) if sym in ["SPX","NDX"] else int(round(last))
EOM

echo "? 8. Clean up empty dirs"
find . -type d -empty -delete

echo "?? Cleanup complete!"
EOF
