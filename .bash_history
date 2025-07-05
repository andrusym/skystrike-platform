+from backend.services.rounding_util import round_to_increment
+from backend.services.option_lookup import get_tradier_option_symbol
@@ async def build_order(...)
-    short_strike = round(spot * 0.96, 0)
-    long_strike  = short_strike - 2
+    short_strike = round_to_increment(spot * 0.96, 0.5)
+    long_strike  = short_strike - 2
--- a/backend/bots/gridbot.py
+++ b/backend/bots/gridbot.py
@@ import logging
-from datetime import date, timedelta
+from datetime import date, timedelta
+from backend.services.rounding_util import round_to_increment
+from backend.services.option_lookup import get_tradier_option_symbol
@@ async def build_order(...)
-    short_strike = round(spot * 0.90, 0)
-    long_strike  = round(spot * 0.85, 0)
+    short_strike = round_to_increment(spot * 0.90, 0.5)
+    long_strike  = round_to_increment(spot * 0.85, 0.5)
--- a/backend/bots/momentumbot.py
+++ b/backend/bots/momentumbot.py
@@ import logging
-from datetime import date, timedelta
+from datetime import date, timedelta
+from backend.services.rounding_util import round_to_increment
+from backend.services.option_lookup import get_tradier_option_symbol
@@ async def build_order(...)
-    short_strike = round(spot * 1.02, 0)
-    long_strike  = round(spot * 1.015,0)
+    short_strike = round_to_increment(spot * 1.02,  0.5)
+    long_strike  = round_to_increment(spot * 1.015, 0.5)
--- a/backend/bots/scalper.py
+++ b/backend/bots/scalper.py
@@ import logging
-from datetime import date, timedelta
+from datetime import date, timedelta
+from backend.services.rounding_util import round_to_increment
+from backend.services.option_lookup import get_tradier_option_symbol
@@ async def build_order(...)
-    short_strike = round(spot * 0.995, 0)
-    long_strike  = round(spot * 0.99,  0)
+    short_strike = round_to_increment(spot * 0.995, 0.5)
+    long_strike  = round_to_increment(spot * 0.99,  0.5)
EOF

# 2. Apply the patch
git apply wire-rounding.patch
# 3. Run your bot tests to confirm
python3 -m backend.scripts.test_all_bots
# 1. From your project root, create the patch file:
cat > wire-rounding.patch << 'EOF'
<PASTE THE ENTIRE PATCH HERE — all diff hunks for iron_condor.py, kingcondor.py, spread.py, …, pairstrader.py>
EOF

# 2. Apply it:
git apply wire-rounding.patch
# 3. (Optional) Clean up:
rm wire-rounding.patch
# 4. Re-run your tests:
python3 -m backend.scripts.test_all_bots
# 0) Make sure any bad patch is gone
rm -f wire-rounding.patch
# 1) Create the patch file (paste only the diff hunks – do NOT run tests here!)
cat > wire-rounding.patch << 'EOF'
--- a/backend/bots/iron_condor.py
+++ b/backend/bots/iron_condor.py
@@ -1,6 +1,9 @@
 import logging
-from typing import Dict, Any
+from typing import Dict, Any
+from datetime import date, timedelta
+from backend.services.rounding_util import round_to_increment
+from backend.services.option_lookup import get_tradier_option_symbol
 from backend.services.tradier_client import TradierClient

@@ async def build_order(ticker: str, contracts: int, dte: int, mode: str) -> Dict[str, Any]:
-    put_short   = round(spot * 0.97, 0)
+    put_short  = round_to_increment(spot * 0.97, 0.5)
@@
-    call_long   = call_short + 5
+    call_long  = call_short + 5
+    sym_ps = get_tradier_option_symbol(ticker, expiration, put_short,  "P")
+    sym_pl = get_tradier_option_symbol(ticker, expiration, put_long,   "P")
+    sym_cs = get_tradier_option_symbol(ticker, expiration, call_short, "C")
+    sym_cl = get_tradier_option_symbol(ticker, expiration, call_long,  "C")
     legs = {
-        "option_symbol[0]": format_option_symbol(ticker, expiration, "P", put_short),
+        "option_symbol[0]": sym_ps,
         "option_symbol[1]": sym_pl,
-        "option_symbol[2]": format_option_symbol(ticker, expiration, "C", call_short),
-        "option_symbol[3]": format_option_symbol(ticker, expiration, "C", call_long),
+        "option_symbol[2]": sym_cs,
+        "option_symbol[3]": sym_cl,
     }

--- a/backend/bots/kingcondor.py
+++ b/backend/bots/kingcondor.py
@@ -1,6 +1,8 @@
 import logging
-from datetime import date, timedelta
+from datetime import date, timedelta
+from backend.services.rounding_util import round_to_increment
+from backend.services.option_lookup import get_tradier_option_symbol
 from backend.services.tradier_client import TradierClient

@@ async def build_order(ticker: str, contracts: int, dte: int, mode: str) -> Dict[str, Any]:
-    put_short   = round(spot * 0.975, 0)
+    put_short  = round_to_increment(spot * 0.975, 0.5)
@@
-    legs = {
+    sym_ps = get_tradier_option_symbol(ticker, expiration, put_short,  "P")
+    sym_pl = get_tradier_option_symbol(ticker, expiration, put_long,   "P")
+    sym_cs = get_tradier_option_symbol(ticker, expiration, call_short, "C")
+    sym_cl = get_tradier_option_symbol(ticker, expiration, call_long,  "C")
+    legs = {
         "option_symbol[0]": sym_ps,
         "option_symbol[1]": sym_pl,
         "option_symbol[2]": sym_cs,
         "option_symbol[3]": sym_cl,
     }

--- a/backend/bots/spread.py
+++ b/backend/bots/spread.py
@@ -1,6 +1,8 @@
 import logging
-from datetime import date, timedelta
+from datetime import date, timedelta
+from backend.services.rounding_util import round_to_increment
+from backend.services.option_lookup import get_tradier_option_symbol
 from backend.services.tradier_client import TradierClient

@@ async def build_order(…):
-    short_strike = round(spot * 0.95, 0)
+    short_strike = round_to_increment(spot * 0.95, 0.5)
@@
-    legs = {
-        "option_symbol[0]": format_option_symbol(ticker, exp, "P", short_strike),
-        "option_symbol[1]": format_option_symbol(ticker, exp, "P", long_strike),
-    }
+    sym_s = get_tradier_option_symbol(ticker, exp, short_strike, "P")
+    sym_l = get_tradier_option_symbol(ticker, exp, long_strike,  "P")
+    legs = {
+        "option_symbol[0]": sym_s,
+        "option_symbol[1]": sym_l,
+    }

--- a/backend/bots/csp.py
+++ b/backend/bots/csp.py
@@ -1,6 +1,8 @@
 import logging
-from datetime import date, timedelta
+from datetime import date, timedelta
+from backend.services.rounding_util import round_to_increment
+from backend.services.option_lookup import get_tradier_option_symbol
 from backend.services.tradier_client import TradierClient

@@ async def build_order(…):
-    strike = round(spot * 0.9, 0)
-    sym    = format_option_symbol(ticker, exp, "P", strike)
+    strike = round_to_increment(spot * 0.9, 0.5)
+    sym    = get_tradier_option_symbol(ticker, exp, strike, "P")

--- a/backend/bots/wheel.py
+++ b/backend/bots/wheel.py
@@ -1,6 +1,8 @@
 import logging
-from datetime import date, timedelta
+from datetime import date, timedelta
+from backend.services.rounding_util import round_to_increment
+from backend.services.option_lookup import get_tradier_option_symbol
 from backend.services.tradier_client import TradierClient

@@ async def build_order(…):
-    strike = round(spot * 0.88, 0)
-    sym    = format_option_symbol(ticker, exp, "P", strike)
+    strike = round_to_increment(spot * 0.88, 0.5)
+    sym    = get_tradier_option_symbol(ticker, exp, strike, "P")

--- a/backend/bots/trend.py
+++ b/backend/bots/trend.py
@@ -1,6 +1,8 @@
 import logging
-from datetime import date, timedelta
+from datetime import date, timedelta
+from backend.services.rounding_util import round_to_increment
+from backend.services.option_lookup import get_tradier_option_symbol
 from backend.services.tradier_client import TradierClient

@@ async def build_order(…):
-    short_strike = round(spot * 0.98, 0)
-    long_strike  = round(spot * 1.02, 0)
+    short_strike = round_to_increment(spot * 0.98, 0.5)
+    long_strike  = round_to_increment(spot * 1.02, 0.5)
+    sym_s        = get_tradier_option_symbol(ticker, exp, short_strike, "P")
+    sym_l        = get_tradier_option_symbol(ticker, exp, long_strike,  "C")

--- a/backend/bots/replicator.py
+++ b/backend/bots/replicator.py
@@ -1,6 +1,8 @@
 import logging
-from datetime import date, timedelta
+from datetime import date, timedelta
+from backend.services.rounding_util import round_to_increment
+from backend.services.option_lookup import get_tradier_option_symbol
 from backend.services.tradier_client import TradierClient

@@ async def build_order(…):
-    short_strike = round(spot * 0.97, 0)
-    long_strike  = short_strike - 3
+    short_strike = round_to_increment(spot * 0.97, 0.5)
+    long_strike  = short_strike - 3
+    sym_s        = get_tradier_option_symbol(ticker, exp, short_strike, "P")
+    sym_l        = get_tradier_option_symbol(ticker, exp, long_strike,  "P")

--- a/backend/bots/copybot.py
+++ b/backend/bots/copybot.py
@@ -1,6 +1,8 @@
 import logging
-from datetime import date, timedelta
+from datetime import date, timedelta
+from backend.services.rounding_util import round_to_increment
+from backend.services.option_lookup import get_tradier_option_symbol
 from backend.services.tradier_client import TradierClient

@@ async def build_order(…):
-    short_strike = round(spot * 1.01, 0)
-    long_strike  = round(spot * 0.99,  0)
+    short_strike = round_to_increment(spot * 1.01, 0.5)
+    long_strike  = round_to_increment(spot * 0.99, 0.5)

--- a/backend/bots/dcabot.py
+++ b/backend/bots/dcabot.py
@@ -1,6 +1,8 @@
 import logging
-from datetime import date, timedelta
+from datetime import date, timedelta
+from backend.services.rounding_util import round_to_increment
+from backend.services.option_lookup import get_tradier_option_symbol
 from backend.services.tradier_client import TradierClient

@@ async def build_order(…):
-    short_strike = round(spot * 0.96, 0)
-    long_strike  = short_strike - 2
+    short_strike = round_to_increment(spot * 0.96, 0.5)
+    long_strike  = short_strike - 2

--- a/backend/bots/gridbot.py
+++ b/backend/bots/gridbot.py
@@ -1,6 +1,8 @@
 import logging
-from datetime import date, timedelta
+from datetime import date, timedelta
+from backend.services.rounding_util import round_to_increment
+from backend.services.option_lookup import get_tradier_option_symbol
 from backend.services.tradier_client import TradierClient

@@ async def build_order(…):
-    short_strike = round(spot * 0.90, 0)
-    long_strike  = round(spot * 0.85, 0)
+    short_strike = round_to_increment(spot * 0.90, 0.5)
+    long_strike  = round_to_increment(spot * 0.85, 0.5)

--- a/backend/bots/momentumbot.py
+++ b/backend/bots/momentumbot.py
@@ -1,6 +1,8 @@
 import logging
-from datetime import date, timedelta
+from datetime import date, timedelta
+from backend.services.rounding_util import round_to_increment
+from backend.services.option_lookup import get_tradier_option_symbol
 from backend.services.tradier_client import TradierClient

@@ async def build_order(…):
-    short_strike = round(spot * 1.02, 0)
-    long_strike  = round(spot * 1.015,0)
+    short_strike = round_to_increment(spot * 1.02,  0.5)
+    long_strike  = round_to_increment(spot * 1.015, 0.5)

--- a/backend/bots/scalper.py
+++ b/backend/bots/scalper.py
@@ -1,6 +1,8 @@
 import logging
-from datetime import date, timedelta
+from datetime import date, timedelta
+from backend.services.rounding_util import round_to_increment
+from backend.services.option_lookup import get_tradier_option_symbol
 from backend.services.tradier_client import TradierClient

@@ async def build_order(…):
-    short_strike = round(spot * 0.995, 0)
-    long_strike  = round(spot * 0.99,  0)
+    short_strike = round_to_increment(spot * 0.995, 0.5)
+    long_strike  = round_to_increment(spot * 0.99,  0.5)

--- a/backend/bots/pairstrader.py
+++ b/backend/bots/pairstrader.py
@@ -1,6 +1,8 @@
 import logging
-from datetime import date, timedelta
+from datetime import date, timedelta
+from backend.services.rounding_util import round_to_increment
+from backend.services.option_lookup import get_tradier_option_symbol
 from backend.services.tradier_client import TradierClient

@@ async def build_order(…):
-    short_strike = round(current_price * 0.96, 0)
-    long_strike  = short_strike - 5
+    target_short = round_to_increment(current_price * 0.96, 0.5)
+    target_long  = target_short - 5
+    short_sym    = get_tradier_option_symbol(ticker, expiration, target_short, "P")
+    long_sym     = get_tradier_option_symbol(ticker, expiration, target_long,  "P")
+    legs = { "option_symbol[0]": short_sym, "option_symbol[1]": long_sym }
EOF

# 2) Apply it
git apply wire-rounding.patch
# 3) Delete the patch
rm wire-rounding.patch
# 4) Re-run your tests
python3 -m backend.scripts.test_all_bots
patch -p0 < wire-rounding.patch
rm wire-rounding.patch
ls backend/bots/*.py
python3 -m backend.scripts.test_all_bots
# List all bot modules
ls backend/bots/*.py
# Find any bots still doing round(spot…) or round(current_price…)
grep -R -nE "round\(.+spot|round\(.+current_price" backend/bots
# Find any bots still calling format_option_symbol directly
grep -R -n "format_option_symbol" backend/bots
python3 -m backend.scripts.test_all_bots
# List any bots still calling the old helper or doing manual round(…)
grep -R -nE "format_option_symbol|round\(" backend/bots/*.py
#!/usr/bin/env bash
set -e
# List of all bots you still need to wire
FILES=(   breakoutbot.py   calendarbot.py   copybot.py   csp.py   dcabot.py   earningsbot.py   gammafly.py   gridbot.py   iron_condor.py   kingcondor.py   momentumbot.py   pairstrader.py   ratioflybot.py   replicator.py   scalper.py   spread.py   squeezehunter.py   straddlebot.py   trend.py   volharvest.py   wheel.py )
for f in "${FILES[@]}"; do   FILE="backend/bots/$f";   echo "Patching $FILE…"
  if ! grep -q "round_to_increment" "$FILE"; then     sed -i '1,/^import/s|import|import\
from backend.services.rounding_util import round_to_increment\
from backend.services.option_lookup    import get_tradier_option_symbol\
|' "$FILE";   fi
  sed -i -E 's/round\(([^(,]+),\s*0\)/round_to_increment(\1, 0.5)/g' "$FILE"
  sed -i -E 's/format_option_symbol\(([^\)]+)\)/get_tradier_option_symbol(\1)/g' "$FILE"; done
echo "All files patched. Now re-run your tests:"
echo "    python3 -m backend.scripts.test_all_bots"
echo "All files patched. Now re-run your tests:"
echo "    python3 -m backend.scripts.test_all_bots"
chmod +x wire_missing_bots.sh
./wire_missing_bots.sh
python3 -m backend.scripts.test_all_bots
cd ~/skystrike_fullstack_final_release/backend
python3 -m backend.scripts.test_all_bots
cd ~/skystrike_fullstack_final_release        # your project root
python3 -m backend.scripts.test_all_bots      # now backend/ is discoverable
python3 -m backend.scripts.test_all_bots
export TRADIER_MODE=paper
python3 -m backend.scripts.test_all_bots
cd ~/skystrike_fullstack_final_release
# Find any lines that are exactly "import" and delete them
grep -R -n '^import$' backend/bots/ | cut -d: -f1 | uniq |   xargs -I{} sed -i '/^import$/d' {}
export TRADIER_MODE=paper
python3 -m backend.scripts.test_all_bots
import logging
from typing import Dict, Any
from datetime import date, timedelta
from backend.services.rounding_util import round_to_increment
from backend.services.option_lookup import get_tradier_option_symbol
from backend.services.tradier_client import TradierClient
cd ~/skystrike_fullstack_final_release
export TRADIER_MODE=paper
python3 -m backend.scripts.test_all_bots
# From your project root
# 1) Turn the stray “logging” line into a proper import
sed -i 's/^logging$/import logging/' backend/bots/iron_condor.py
# 2) Make sure TRADIER_MODE is set to paper
export TRADIER_MODE=paper
# 3) Re-run the full bot test suite
python3 -m backend.scripts.test_all_bots
chmod +x backend/scripts/test_all_bots.py
export TRADIER_MODE=paper
python3 -m backend.scripts.test_all_bots
find backend/bots -type f -name '*.py' -exec sed -i '/^[[:blank:]]*logging\s*$/d' {} +
python3 -m backend.scripts.test_all_bots
# 1) Remove any lines that are just "logging"
find backend/bots -type f -name '*.py' -exec sed -i '/^[[:blank:]]*logging\s*$/d' {} +
# 2) Insert "import logging" at the top of any file that doesn't already import it
for f in backend/bots/*.py; do   grep -q '^import logging' "$f" || sed -i '1i import logging' "$f"; done
python3 -m backend.scripts.test_all_bots
# Remove lines where an import ends with no symbols
find backend/bots -type f -name '*.py' -exec sed -i '/from .* import[[:space:]]*$/d' {} +
# Now verify
python3 -m backend.scripts.test_all_bots
# Delete lines that consist of only one bare identifier (possibly indented)
find backend/bots -type f -name '*.py' -exec sed -i '/^[[:blank:]]*[A-Za-z_][A-Za-z0-9_]*[[:blank:]]*$/d' {} +
# Rerun the full bot test suite
python3 -m backend.scripts.test_all_bots
sed -i '/"""/d' backend/bots/runner.py
python3 -m backend.scripts.test_all_bots
sed -i "/Dispatch to the appropriate bot's build_order/d" backend/bots/runner.py
python3 -m backend.scripts.test_all_bots
mv backend/bots/runner.py backend/bots/runner.py.bak
python3 -m backend.scripts.test_all_bots
# For each bot file that lacks the TradierClient import, add it at the top
grep -L "TradierClient" backend/bots/*.py   | xargs -I{} sed -i '1i from backend.services.tradier_client import TradierClient' {}
# Now rerun the full suite
python3 -m backend.scripts.test_all_bots
grep -Rl "TradierClient" backend/bots/*.py   | xargs grep -L "from backend.services.tradier_client import TradierClient"   | xargs -I{} sed -i '1i from backend.services.tradier_client import TradierClient' {}
python3 -m backend.scripts.test_all_bots
cat << 'EOF' | patch -p1
*** Begin Patch
*** Update File: backend/services/tradier_client.py
@@ def format_option(self, ticker: str, expiration: str, callput: str, strike: float) -> str:
-        date_fmt = datetime.strptime(expiration, "%Y-%m-%d").strftime("%y%m%d")
+        # normalize expiration string (allow both YYYYMMDD and YYYY-MM-DD formats)
+        if expiration.isdigit() and len(expiration) == 8:
+            expiration = f"{expiration[:4]}-{expiration[4:6]}-{expiration[6:8]}"
+        date_fmt = datetime.strptime(expiration, "%Y-%m-%d").strftime("%y%m%d")
*** End Patch
EOF

python3 -m backend.scripts.test_all_bots
patch -p0 << 'EOF'
*** Begin Patch
*** Update File: backend/services/tradier_client.py
@@ def format_option(self, ticker: str, expiration: str, callput: str, strike: float) -> str:
-        date_fmt = datetime.strptime(expiration, "%Y-%m-%d").strftime("%y%m%d")
+        # normalize expiration string (allow YYYYMMDD or YYYY-MM-DD)
+        if expiration.isdigit() and len(expiration) == 8:
+            expiration = f"{expiration[0:4]}-{expiration[4:6]}-{expiration[6:8]}"
+        date_fmt = datetime.strptime(expiration, "%Y-%m-%d").strftime("%y%m%d")
*** End Patch
EOF

python3 -m backend.scripts.test_all_bots
patch -p0 << 'EOF'
*** Begin Patch
*** Update File: backend/services/tradier_client.py
@@ def format_option(self, ticker: str, expiration: str, callput: str, strike: float) -> str:
-        date_fmt = datetime.strptime(expiration, "%Y-%m-%d").strftime("%y%m%d")
+        # normalize expiration (allow YYYYMMDD or YYYY-MM-DD)
+        if expiration.isdigit() and len(expiration) == 8:
+            expiration = f"{expiration[:4]}-{expiration[4:6]}-{expiration[6:8]}"
+        date_fmt = datetime.strptime(expiration, "%Y-%m-%d").strftime("%y%m%d")
*** End Patch
EOF

python3 -m backend.scripts.test_all_bots
ed -s backend/services/tradier_client.py << 'EOF'
/date_fmt = datetime.strptime(expiration, "%Y-%m-%d")
a
        # accept YYYYMMDD by converting to YYYY-MM-DD
        if expiration.isdigit() and len(expiration) == 8:
            expiration = f"{expiration[:4]}-{expiration[4:6]}-{expiration[6:8]}"
.
w
EOF

# now re-run your tests
python3 -m backend.scripts.test_all_bots
sed -i '/date_fmt = datetime.strptime/i \
        # accept YYYYMMDD by converting to YYYY-MM-DD\
        if expiration.isdigit() and len(expiration) == 8:\
            expiration = f"{expiration[:4]}-{expiration[4:6]}-{expiration[6:8]}"' backend/services/tradier_client.py
python3 -m backend.scripts.test_all_bots
--- a/backend/services/tradier_client.py
+++ b/backend/services/tradier_client.py
@@ -122,7 +122,16 @@ class TradierClient:
-        date_fmt = datetime.strptime(expiration, "%Y-%m-%d").strftime("%y%m%d")
+        # support both "YYYY-MM-DD" and "YYYYMMDD" expiration strings
+        try:
+            exp_date = datetime.strptime(expiration, "%Y-%m-%d")
+        except ValueError:
+            # fallback for expiration codes like "20250704"
+            exp_date = datetime.strptime(expiration, "%Y%m%d")
+        date_fmt   = exp_date.strftime("%y%m%d")
python3 -m backend.scripts.test_all_bots
git remote add origin https://github.com/andrusym/skystrike-platform.git
git branch -M main
git push -u origin main
git pull origin main
git push -u origin main
git pull origin main --no-rebase
git add .
git commit -m "Resolved merge conflicts"
git push -u origin main
git pull origin main --no-rebase
git add .
git commit -m "Merged remote changes"
nano .gitignore
git rm -r --cached .
git add .
git commit -m "Clean up repository and add proper .gitignore"
git pull origin main --no-rebase
git add .
git commit -m "Merged remote main into local"
git push -u origin main
git add .
git commit -m "Merged remote changes into local branch"
nano .gitignore
git rm -r --cached .
git add .
git commit -m "Clean up repo and apply .gitignore"
nano .gitignore  # paste the above contents and save
git rm -r --cached .
git add .
git commit -m "Update .gitignore to ignore unnecessary files"
git push -u origin main
git pull origin main
git push -u origin main --force
git pull origin main
git add .
git commit -m "Merged remote main into local"
git push origin main
git push origin main --force
# First, remove existing remote if it already exists
git remote remove origin
# Now, add the new repository as the remote origin
git remote add origin https://github.com/andrusym/skystrike-platform.git
# Stage all your changes
git add .
# Commit changes (if you haven't already committed)
git commit -m "Initial commit to skystrike-platform repo"
# Push your changes to the new repo
git push -u origin main
Username for 'https://github.com':
git push https://andrusym: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@github.com/andrusym/skystrike-platform.git
git reset HEAD .github/workflows/deploy.yml
git restore --staged .github/workflows/deploy.yml
git push
git push https://andrusym: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@github.com/andrusym/skystrike-platform.git
cat > .gitignore << 'EOF'
# Python
venv/
__pycache__/
*.py[cod]
*.pyo
*.pyd
*.pyc
*.pdb
*.egg
*.egg-info/
dist/
build/

# Node/Vite frontend
node_modules/
.npm/
.yarn/
*.log
.vite/
.vitepress/
*.tsbuildinfo

# PM2 logs and runtime
.pm2/
bot_run.log
*.log

# System
.DS_Store
*.swp
*.swo
*.bak
*.tmp
*.zip
*.history
*.sqlite_history
*.python_history
*.env
.env.*

# Editor configs
.idea/
.vscode/
*.code-workspace

# Jupyter and notebooks
.ipynb_checkpoints/
*.ipynb

# GitHub files (for safety)
.github/workflows/*-example.yml

# Local compiled binaries or shared libs
*.so
*.dll
*.dylib
*.out

# Specific binaries and problematic files
.local/
skystrike-data/
default-ssl.conf
skystrike_fullstack_final_release.zip
EOF

git add .gitignore
git commit -m "Updated .gitignore to exclude logs, builds, and envs"
git push
git push --set-upstream origin main
git remote set-url origin https://andrusym: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@github.com/andrusym/skystrike-platform.git
git push --set-upstream origin main
nano .gitignore  # paste the above contents and savepython3 -m backend.scripts.test_all_bots
python3 -m backend.scripts.test_all_bots
curl -X GET "https://sandbox.tradier.com/v1/accounts/VA70062258/orders/18206574"   -H "Authorization: Bearer RlLmD2V8FKCJAcuj9KQoKpU5TeKt"   -H "Accept: application/json"
curl -X GET "https://sandbox.tradier.com/v1/accounts/VA70062258/orders"   -H "Authorization: Bearer RlLmD2V8FKCJAcuj9KQoKpU5TeKt"   -H "Accept: application/json"
import requests
TRADIER_API_URL = "https://sandbox.tradier.com/v1"
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
ACCOUNT_ID = "YOUR_ACCOUNT_ID"
headers = {
}
# Step 1: Get open orders
def get_open_orders():
# Step 2: Cancel each open order
def cancel_order(order_id):
# Execute cancellation
open_orders = get_open_orders()
if not open_orders:;     print("No open orders to cancel.")
else:
nano cancel_all_orders.py
python3 cancel_all_orders.py
curl -X GET "https://sandbox.tradier.com/v1/accounts/VA70062258/orders"   -H "Authorization: Bearer RlLmD2V8FKCJAcuj9KQoKpU5TeKt"   -H "Accept: application/json"
python3 cancel_all_orders.py
curl -X GET "https://sandbox.tradier.com/v1/accounts/VA70062258/orders"   -H "Authorization: Bearer RlLmD2V8FKCJAcuj9KQoKpU5TeKt"   -H "Accept: application/json"
GET /v1/accounts/{account_id}/orders
Host: sandbox.tradier.com
Authorization: Bearer {ACCESS_TOKEN}
curl -X GET "https://sandbox.tradier.com/v1/accounts/YOUR_ACCOUNT_ID/orders"   -H "Authorization: Bearer YOUR_ACCESS_TOKEN"   -H "Accept: application/json"
export $(grep -v '^#' .env | xargs) && curl -X GET "https://sandbox.tradier.com/v1/accounts/$TRADIER_ACCOUNT_ID/orders"   -H "Authorization: Bearer $TRADIER_TOKEN"   -H "Accept: application/json"
curl http://localhost:8000/api/login   -H "Content-Type: application/json"   -d '{"username":"admin","password":"webflow"}'
curl -X GET "https://sandbox.tradier.com/v1/accounts/$TRADIER_ACCOUNT_ID/orders"   -H "Authorization: Bearer $TRADIER_TOKEN"   -H "Accept: application/json"
nano ~/skystrike_fullstack_final_release/backend/.env
export $(grep -v '^#' .env | xargs)
export TRADIER_TOKEN=$TRADIER_SANDBOX_ACCESS_TOKEN
export TRADIER_ACCOUNT_ID=$TRADIER_SANDBOX_ACCOUNT_ID
curl -X GET "https://sandbox.tradier.com/v1/accounts/$TRADIER_ACCOUNT_ID/orders"   -H "Authorization: Bearer $TRADIER_TOKEN"   -H "Accept: application/json"
python3 scripts/cancel_all_orders.py
cd ~/skystrike_fullstack_final_release/backend
python3 scripts/cancel_all_orders.py
cd ~/skystrike_fullstack_final_release
python3 backend/scripts/cancel_all_orders.py
crontab -e
git push
cd ~/skystrike_fullstack_final_release
git status
git push origin main --force
# Ensure you're on main
git checkout main
# Stage ALL local changes (add new + modified + deletions)
git add --all
# Commit all changes
git commit -m "Force overwrite GitHub with local version"
# Force push to overwrite GitHub
git push origin main --force
-26-1-2:~/skystrike_fullstack_final_release$ git push origin main --force
cd ~/skystrike_fullstack_final_release
python3 backend/scripts/run_all_bots.py
python3 backend/scripts/test_all_bots.py
PYTHONPATH=. python3 backend/scripts/test_all_bots.py
nano ~/skystrike_fullstack_final_release/backend/.env
PYTHONPATH=. python3 backend/scripts/test_all_bots.py
ps aux | grep -E 'python|uvicorn'
# Then:
kill -9 <PID>   # only for any old zombie PIDs
cd ~/skystrike_fullstack_final_release/logs
# Remove temporary junk
rm -f *.log.* *.bak *.tmp
# Archive logs older than 7 days
mkdir -p archive
find . -name "*.log" -mtime +7 -exec mv {} archive/ \;
cd ~/skystrike_fullstack_final_release
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -name "*.pyc" -delete
source venv/bin/activate
pip freeze > requirements.txt
pip install -r requirements.txt   # (Optional reinstall)
chmod 600 .env
chmod 700 backend/scripts/*.py
crontab -l             # Sanity check
sudo systemctl restart cron
# If using PM2:
pm2 restart all
# If using systemd:
sudo systemctl restart skystrike
sudo apt update && sudo apt upgrade -y
sudo apt autoremove -y
sudo apt update && sudo apt upgrade -y
sudo apt autoremove -y
tail -n 100 logs/*.log
cd ~/skystrike_fullstack_final_release
python3 -m backend.scripts.ml_live_loop
cd ~/skystrike_fullstack_final_release && PYTHONPATH=. python3 -m backend.scripts.ml_live_loop.py
mv backend/ml_live_loop.py backend/scripts/ml_live_loop.py
cd ~/skystrike_fullstack_final_release
PYTHONPATH=. python3 -m backend.scripts.ml_live_loop
mv backend/schedulers/"goal aware shift engine.py" backend/schedulers/goal_aware_shift_engine.py
mv "backend/schedulers/goal aware shift engine.py" backend/schedulers/goal_aware_shift_engine.py
ls backend/schedulers/
python3 backend/scripts/goal_aware_shift_engine.py
python3 backend/schedulers/goal_aware_shift_engine.py
crontab -e
mv backend/scripts/ml_live_loop.py backend/schedulers/
mv backend/scripts/market_watcher.py backend/schedulers/
cd ~/skystrike_fullstack_final_release
PYTHONPATH=. python3 -m backend.schedulers.self_tuning_engine
PYTHONPATH=. python3 backend/scripts/test_all_bots.py
python3 backend/scripts/cancel_all_orders.py
ls -la ml/
ls -la schedulers/
ls -la engine/
# Move ml files
mkdir -p backend/ml
mv ml/*.py backend/ml/
# Move scheduler files
mkdir -p backend/schedulers
mv schedulers/*.py backend/schedulers/
# (Optional) Move engine files if used
mkdir -p backend/engine
mv engine/*.py backend/engine/
PYTHONPATH=. python3 backend/scripts/test_all_bots.py
python3 backend/scripts/cancel_all_orders.py
mv backend/config/wealth_config.json backend/data/wealth_config.json
grep -rnw backend/ -e 'config/wealth_config.json'
nano backend/diagnostics/validate_files.py
sed -i 's|config/wealth_config.json|data/wealth_config.json|g' backend/diagnostics/validate_files.py
grep -rnw backend/ -e 'config/wealth_config.json'
find . -type d -empty
find . -type d | sed 's|.*/||' | sort | uniq -d
find backend/ -type d | sed 's|.*/||' | sort | uniq -d
PYTHONPATH=. python3 backend/scripts/test_all_bots.py
# Run full orchestrator every 15 min
*/15 * * * * /usr/bin/python3 /home/ubuntu/skystrike_fullstack_final_release/backend/scripts/run_orchestration.py >> /home/ubuntu/logs/orch.log 2>&1
# Run midday condor bots (0DTE)
0 12 * * 1-5 /bin/bash /home/ubuntu/skystrike_fullstack_final_release/backend/scripts/midday_bot_runner.sh >> /home/ubuntu/logs/midday.log 2>&1
# Run nightly self-tuner + apply config
0 4 * * * /usr/bin/python3 /home/ubuntu/skystrike_fullstack_final_release/backend/scripts/apply_final_recommendation.py >> /home/ubuntu/logs/rebalance.log 2>&1
# Edit crontab:
crontab -e
which python3
cd backend
python3 engine/orchestration_engine.py
cd ~/skystrike_fullstack_final_release
PYTHONPATH=. venv/bin/python3 backend/engine/orchestration_engine.py
PYTHONPATH=. python3 backend/scripts/test_all_bots.py
uvicorn backend.main:app --reload
pip install yfinance
uvicorn backend.main:app --reload
PYTHONPATH=. python3 backend/scripts/test_all_bots.py
cat > backend/engine/risk_budget_engine.py << 'EOF'
# backend/engine/risk_budget_engine.py

"""
Risk Budget Engine: enforces maximum portfolio risk limits based on volatility regime.
"""

import logging
from typing import Dict, Any

from .volatility_engine import get_vix_level, classify_volatility_regime

logger = logging.getLogger(__name__)

def enforce_risk_budget(config: Dict[str, Any], max_risk: float = 0.1) -> Dict[str, Any]:
    """
    Adjusts bot contract allocations to ensure overall portfolio risk 
    does not exceed max_risk threshold. Uses volatility regime as a proxy.
    
    Args:
        config: dict mapping bot names to their config dicts, including 'contracts'.
        max_risk: float, maximum allowable risk level (0 to 1).

    Returns:
        Adjusted config dict with potentially reduced 'contracts' for riskier regimes.
    """
    vix = get_vix_level()
    regime = classify_volatility_regime(vix)
    logger.info(f"Current VIX level: {vix}, regime: {regime}, applying max_risk={max_risk}")

    adjusted_config = {}
    for bot, conf in config.items():
        original = conf.get("contracts", 0)
        # Example rule: in 'extreme' regime, cap contracts to half
        if regime == "extreme":
            adjusted = int(original * (1 - max_risk))
        elif regime == "high":
            adjusted = int(original * (1 - max_risk / 2))
        else:
            adjusted = original
        adjusted_config[bot] = {**conf, "contracts": adjusted}
    logger.info(f"Risk budget applied: {adjusted_config}")
    return adjusted_config

__all__ = ["enforce_risk_budget"]
EOF

# Now restart and retest:
uvicorn backend.main:app --reload
PYTHONPATH=. python3 backend/scripts/test_all_bots.py
# Replace your volatility_engine.py with proper definitions for get_vix_level and classify_volatility_regime
cat > backend/engine/volatility_engine.py << 'EOF'
# backend/engine/volatility_engine.py

\"\"\"
Volatility Engine: fetches current VIX level and classifies regime.
\"\"\"

import logging

logger = logging.getLogger(__name__)

def get_vix_level() -> float:
    \"\"\"
    Fetch the latest VIX close price using yfinance.
    \"\"\"
    try:
        import yfinance as yf
    except ImportError:
        msg = (
            "Missing dependency 'yfinance'.\\n"
            "Install it with: pip install yfinance"
        )
        logger.error(msg)
        raise ImportError(msg)

    try:
        vix = yf.Ticker("^VIX")
        hist = vix.history(period="1d")
        if hist.empty:
            raise ValueError("No VIX data available")
        return float(hist["Close"].iloc[-1])
    except Exception as e:
        logger.warning(f"VIX fetch failed: {e}. Using default VIX=20.0")
        return 20.0

def classify_volatility_regime(vix: float) -> str:
    \"\"\"
    Classify volatility regime based on VIX value.
    \"\"\"
    if vix < 15:
        return "low"
    elif vix < 25:
        return "moderate"
    elif vix < 35:
        return "high"
    else:
        return "extreme"

__all__ = ["get_vix_level", "classify_volatility_regime"]
EOF

# Install yfinance if you haven't already
pip install yfinance
# Restart the API and rerun the tests
uvicorn backend.main:app --reload &  
sleep 2  
PYTHONPATH=. python3 backend/scripts/test_all_bots.py
# Overwrite backend/engine/volatility_engine.py with correct triple-quotes (no backslashes)
cat > backend/engine/volatility_engine.py << 'EOF'
# backend/engine/volatility_engine.py

"""
Volatility Engine: fetches current VIX level and classifies regime.
"""

import logging

logger = logging.getLogger(__name__)

def get_vix_level() -> float:
    """
    Fetch the latest VIX close price using yfinance.
    """
    try:
        import yfinance as yf
    except ImportError:
        msg = (
            "Missing dependency 'yfinance'.\n"
            "Install it with: pip install yfinance"
        )
        logger.error(msg)
        raise ImportError(msg)

    try:
        vix = yf.Ticker("^VIX")
        hist = vix.history(period="1d")
        if hist.empty:
            raise ValueError("No VIX data available")
        return float(hist["Close"].iloc[-1])
    except Exception as e:
        logger.warning(f"VIX fetch failed: {e}. Using default VIX=20.0")
        return 20.0

def classify_volatility_regime(vix: float) -> str:
    """
    Classify volatility regime based on VIX value.
    """
    if vix < 15:
        return "low"
    elif vix < 25:
        return "moderate"
    elif vix < 35:
        return "high"
    else:
        return "extreme"

__all__ = ["get_vix_level", "classify_volatility_regime"]
EOF

# Install yfinance if needed
pip install yfinance
# Restart the API (stop existing and start fresh)
pkill -f 'uvicorn' || true
uvicorn backend.main:app --reload &
# Allow time to spin up
sleep 2
# Run the bot test script again
PYTHONPATH=. python3 backend/scripts/test_all_bots.py
# 1. Overwrite runner_dispatcher.py with the correct dispatch_bot_by_name implementation
cat > backend/engine/runner_dispatcher.py << 'EOF'
# backend/engine/runner_dispatcher.py

import logging
from backend.engine.bot_entry_engine import BOT_BUILDERS

logger = logging.getLogger(__name__)

def dispatch_bot_by_name(bot_name: str, *args, **kwargs):
    \"\"\"
    Build and submit a single bot order by name.
    \"\"\"
    if bot_name not in BOT_BUILDERS:
        raise ValueError(f"No builder found for bot: {bot_name}")

    module_path, fn_name = BOT_BUILDERS[bot_name]
    module = __import__(module_path, fromlist=[fn_name])
    build_fn = getattr(module, fn_name)

    logger.info(f"Building order for bot: {bot_name}")
    order_payload = build_fn(*args, **kwargs)

    # lazy import to avoid circular dependency
    from backend.submit_order import run_bot_with_params

    logger.info(f"Submitting order for bot: {bot_name}")
    run_bot_with_params(bot_name, order_payload)
    return order_payload
EOF

# 2. Restart your FastAPI server
pkill -f uvicorn || true
uvicorn backend.main:app --reload &
# Give it a moment to start
sleep 2
# 3. Re-run your bot tests
PYTHONPATH=. python3 backend/scripts/test_all_bots.py
# Overwrite runner_dispatcher.py without backslashes before the docstring
cat > backend/engine/runner_dispatcher.py << 'EOF'
# backend/engine/runner_dispatcher.py

import logging
from backend.engine.bot_entry_engine import BOT_BUILDERS

logger = logging.getLogger(__name__)

def dispatch_bot_by_name(bot_name: str, *args, **kwargs):
    """
    Build and submit a single bot order by name.
    """
    if bot_name not in BOT_BUILDERS:
        raise ValueError(f"No builder found for bot: {bot_name}")

    module_path, fn_name = BOT_BUILDERS[bot_name]
    module = __import__(module_path, fromlist=[fn_name])
    build_fn = getattr(module, fn_name)

    logger.info(f"Building order for bot: {bot_name}")
    order_payload = build_fn(*args, **kwargs)

    # lazy import to avoid circular dependency
    from backend.submit_order import run_bot_with_params

    logger.info(f"Submitting order for bot: {bot_name}")
    run_bot_with_params(bot_name, order_payload)
    return order_payload

__all__ = ["dispatch_bot_by_name"]
EOF

# Restart FastAPI and re-run the tests
pkill -f uvicorn || true
uvicorn backend.main:app --reload &
# Give it a couple seconds to start
sleep 2
# Run your bot tests again
PYTHONPATH=. python3 backend/scripts/test_all_bots.py
# 1. Patch trading_engine.py to import from the correct path
cat > backend/engine/trading_engine.py << 'EOF'
# backend/engine/trading_engine.py

\"\"\"
Trading Engine: executes a built order payload via the submit_order module.
\"\"\"

import logging
from typing import Dict, Any

from backend.submit_order import run_bot_with_params

logger = logging.getLogger(__name__)

def execute_trade(bot_name: str, order_payload: Dict[str, Any]) -> None:
    \"\"\"
    Execute a single trade for the given bot.
    \"\"\"
    try:
        logger.info(f"Executing trade for bot: {bot_name} with payload: {order_payload}")
        run_bot_with_params(bot_name, order_payload)
    except Exception as e:
        logger.error(f"Failed to execute trade for {bot_name}: {e}")
        raise

__all__ = ["execute_trade"]
EOF

# 2. Restart Uvicorn (stop any existing and start fresh)
pkill -f uvicorn || true
uvicorn backend.main:app --reload &
# Give it a moment to spin up
sleep 2
# 3. Re-run your bot orchestration tests
PYTHONPATH=. python3 backend/scripts/test_all_bots.py
# Overwrite trading_engine.py with proper triple-quoted docstrings
cat > backend/engine/trading_engine.py << 'EOF'
# backend/engine/trading_engine.py

"""
Trading Engine: executes a built order payload via the submit_order module.
"""

import logging
from typing import Dict, Any

from backend.submit_order import run_bot_with_params

logger = logging.getLogger(__name__)

def execute_trade(bot_name: str, order_payload: Dict[str, Any]) -> None:
    """
    Execute a single trade for the given bot.
    """
    try:
        logger.info(f"Executing trade for bot: {bot_name} with payload: {order_payload}")
        run_bot_with_params(bot_name, order_payload)
    except Exception as e:
        logger.error(f"Failed to execute trade for {bot_name}: {e}")
        raise

__all__ = ["execute_trade"]
EOF

# Restart the FastAPI server (stop any running instance first)
pkill -f uvicorn || true
uvicorn backend.main:app --reload &
# Give the server time to spin up
sleep 2
# Re-run your bot test script
PYTHONPATH=. python3 backend/scripts/test_all_bots.py
# 1. Patch adaptive_sizing_engine.py to define adjust_contract_size
cat > backend/engine/adaptive_sizing_engine.py << 'EOF'
# backend/engine/adaptive_sizing_engine.py

\"\"\"
Adaptive Sizing Engine: scales contract counts based on provided multiplier or ML confidence.
\"\"\"

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def adjust_contract_size(
    config: Dict[str, Any],
    multiplier: float = 1.0
) -> Dict[str, Any]:
    \"\"\"
    Multiply each bot's contract count by `multiplier`.
    E.g. to bump size by 10%, use multiplier=1.1.
    \"\"\"
    adjusted = {}
    for bot, conf in config.items():
        base = conf.get("contracts", 0)
        new_ct = int(base * multiplier)
        adjusted[bot] = {**conf, "contracts": new_ct}
    logger.info(f"Adjusted contract sizes with multiplier {multiplier}: {adjusted}")
    return adjusted

__all__ = ["adjust_contract_size"]
EOF

# 2. Patch trading_engine.py to lazy-import run_bot_with_params and avoid circular import
cat > backend/engine/trading_engine.py << 'EOF'
# backend/engine/trading_engine.py

\"\"\"
Trading Engine: executes a built order payload via the submit_order module.
\"\"\"

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def execute_trade(bot_name: str, order_payload: Dict[str, Any]) -> None:
    \"\"\"
    Execute a single trade for the given bot.
    \"\"\"
    try:
        # Lazy import to break circular dependency
        from backend.submit_order import run_bot_with_params
        logger.info(f"Executing trade for bot: {bot_name} with payload: {order_payload}")
        run_bot_with_params(bot_name, order_payload)
    except Exception as e:
        logger.error(f"Failed to execute trade for {bot_name}: {e}")
        raise

__all__ = ["execute_trade"]
EOF

# 3. Restart your FastAPI server
pkill -f uvicorn || true
uvicorn backend.main:app --reload &
# 4. Give it a moment to start, then re-run your test suite
sleep 2
PYTHONPATH=. python3 backend/scripts/test_all_bots.py
# 1. Re-write trading_engine.py with clean triple-quoted docstrings
cat > backend/engine/trading_engine.py << 'EOF'
# backend/engine/trading_engine.py

"""
Trading Engine: executes a built order payload via the submit_order module.
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def execute_trade(bot_name: str, order_payload: Dict[str, Any]) -> None:
    """
    Execute a single trade for the given bot.
    """
    try:
        # Lazy import to break circular dependency
        from backend.submit_order import run_bot_with_params
        logger.info(f"Executing trade for bot: {bot_name} with payload: {order_payload}")
        run_bot_with_params(bot_name, order_payload)
    except Exception as e:
        logger.error(f"Failed to execute trade for {bot_name}: {e}")
        raise

__all__ = ["execute_trade"]
EOF

# 2. Restart Uvicorn (stop any running instance first)
pkill -f uvicorn || true
uvicorn backend.main:app --reload &
# 3. Give it a few seconds to start
sleep 3
# 4. Re-run your bot tests
PYTHONPATH=. python3 backend/scripts/test_all_bots.py
# Overwrite adaptive_sizing_engine.py with proper triple-quoted docstrings
cat > backend/engine/adaptive_sizing_engine.py << 'EOF'
# backend/engine/adaptive_sizing_engine.py

"""
Adaptive Sizing Engine: scales contract counts based on provided multiplier or ML confidence.
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def adjust_contract_size(
    config: Dict[str, Any],
    multiplier: float = 1.0
) -> Dict[str, Any]:
    """
    Multiply each bot’s contract count by `multiplier`.
    E.g., to bump size by 10%, use multiplier=1.1.
    """
    adjusted = {}
    for bot, conf in config.items():
        base = conf.get("contracts", 0)
        new_ct = int(base * multiplier)
        adjusted[bot] = {**conf, "contracts": new_ct}
    logger.info(f"Adjusted contract sizes with multiplier {multiplier}: {adjusted}")
    return adjusted

__all__ = ["adjust_contract_size"]
EOF

# Restart FastAPI to apply changes
pkill -f uvicorn || true
uvicorn backend.main:app --reload &
# Wait for server to start
sleep 3
# Re-run your bot tests
PYTHONPATH=. python3 backend/scripts/test_all_bots.py
# 1. Overwrite bot_decay_monitor.py with definitions for check_drawdown and should_deactivate_bot
cat > backend/engine/bot_decay_monitor.py << 'EOF'
# backend/engine/bot_decay_monitor.py

"""
Monitor per-bot drawdown and signal deactivation if a threshold is exceeded.
"""

import logging
from typing import Dict

logger = logging.getLogger(__name__)

# Default drawdown threshold (e.g., 0.1 = 10%)
DEFAULT_DRAWDOWN_THRESHOLD = 0.1

# In-memory store of peak P&L per bot
_bot_peaks: Dict[str, float] = {}

def check_drawdown(bot_name: str, current_pnl: float) -> float:
    """
    Calculate the drawdown for a bot:
      drawdown = (peak_pnl - current_pnl) / peak_pnl
    Updates the stored peak if current_pnl exceeds it.
    Returns the drawdown fraction.
    """
    peak = _bot_peaks.get(bot_name, current_pnl)
    if current_pnl > peak:
        _bot_peaks[bot_name] = current_pnl
        peak = current_pnl

    if peak == 0:
        return 0.0

    drawdown = (peak - current_pnl) / peak
    logger.debug(f"Bot '{bot_name}' PnL: {current_pnl}, Peak: {peak}, Drawdown: {drawdown}")
    return drawdown

def should_deactivate_bot(
    bot_name: str,
    current_pnl: float,
    threshold: float = DEFAULT_DRAWDOWN_THRESHOLD
) -> bool:
    """
    Returns True if the bot's drawdown exceeds `threshold`.
    """
    dd = check_drawdown(bot_name, current_pnl)
    if dd > threshold:
        logger.warning(f"Bot '{bot_name}' drawdown {dd:.2%} exceeds threshold {threshold:.2%}.")
        return True
    return False

__all__ = ["check_drawdown", "should_deactivate_bot"]
EOF

# 2. Restart the FastAPI server
pkill -f uvicorn || true
uvicorn backend.main:app --reload &
# Wait a moment for the server to start
sleep 3
# 3. Re-run your bot test script
PYTHONPATH=. python3 backend/scripts/test_all_bots.py
# Patch hybrid_bot.py so build_order requires no positional args
cat > backend/bots/hybrid_bot.py << 'EOF'
# backend/bots/hybrid_bot.py

import logging
from typing import Dict, Any

from backend.engine.dynamic_dte_selector import choose_optimal_dte
from backend.engine.volatility_engine import get_vix_level, classify_volatility_regime
from backend.engine.position_tracker import update_open_positions
from backend.services.tradier_client import TradierClient
from backend.services.option_lookup import get_tradier_option_symbol

logger = logging.getLogger(__name__)

def build_order(bot_name: str = None, ticker: str = "SPY", **kwargs) -> Dict[str, Any]:
    """
    Hybrid bot: chooses Condor vs Trend logic depending on VIX regime.
    'bot_name' is accepted for compatibility but not used.
    Defaults to SPY if no ticker provided.
    """
    # 1. figure out regime
    vix = get_vix_level()  # e.g. 12.5
    regime = classify_volatility_regime(vix)

    # 2. choose dte
    exp_date = choose_optimal_dte(ticker)

    # 3. build the appropriate order payload
    if regime in ("high", "extreme"):
        from backend.bots.iron_condor import build_order as ic_build
        order = ic_build(ticker=ticker, dte=exp_date, **kwargs)
    else:
        from backend.bots.trend import build_order as trend_build
        order = trend_build(ticker=ticker, dte=exp_date, **kwargs)

    # 4. log positions and return
    update_open_positions()  # refresh positions
    logger.info(f"[HybridBot] built order for ticker={ticker}: {order}")
    return order
EOF

# Restart the FastAPI server to apply changes
pkill -f uvicorn || true
uvicorn backend.main:app --reload &
# Give it a few seconds to start
sleep 3
# Re-run your bot tests
PYTHONPATH=. python3 backend/scripts/test_all_bots.py
# Restart the server and rerun tests
pkill -f uvicorn || true
uvicorn backend.main:app --reload &
sleep 3
PYTHONPATH=. python3 backend/scripts/test_all_bots.py
# 1. Patch hybrid_bot.py to compute a numeric DTE instead of passing a date object
cat > backend/bots/hybrid_bot.py << 'EOF'
# backend/bots/hybrid_bot.py

import logging
from datetime import date
from typing import Dict, Any

from backend.engine.dynamic_dte_selector import choose_optimal_dte
from backend.engine.volatility_engine import get_vix_level, classify_volatility_regime
from backend.engine.position_tracker import update_open_positions

logger = logging.getLogger(__name__)

def build_order(bot_name: str = None, ticker: str = "SPY", **kwargs) -> Dict[str, Any]:
    """
    Hybrid bot: chooses Condor vs Trend logic depending on VIX regime.
    Accepts ticker, ignores any passed 'dte' and other extraneous params.
    """
    # Remove any provided dte to avoid conflicts
    kwargs.pop("dte", None)

    # Determine regime
    vix = get_vix_level()
    regime = classify_volatility_regime(vix)

    # Choose expiration date and compute DTE offset
    exp_date = choose_optimal_dte(ticker)           # returns a date object
    dte_days = (exp_date - date.today()).days       # integer days until expiration

    # Build order using appropriate bot logic
    if regime in ("high", "extreme"):
        from backend.bots.iron_condor import build_order as ic_build
        order = ic_build(ticker=ticker, dte=dte_days, **kwargs)
    else:
        from backend.bots.trend import build_order as trend_build
        order = trend_build(ticker=ticker, dte=dte_days, **kwargs)

    # Refresh positions and return
    update_open_positions()
    logger.info(f"[HybridBot] built order for ticker={ticker}, dte={dte_days}: {order}")
    return order
EOF

# 2. Fix the syntax error in bot_metrics_route.py by prepending 'from '
sed -i 's/^utils\.trade_logger import/from utils.trade_logger import/' backend/routes/bot_metrics_route.py
# 3. Restart the server and re-run tests
pkill -f uvicorn || true
uvicorn backend.main:app --reload &
sleep 3
PYTHONPATH=. python3 backend/scripts/test_all_bots.py
# 1. Make sure you're in the project root
cd ~/skystrike_fullstack_final_release
# 2. Run the orchestration entrypoint
PYTHONPATH=. python3 - << 'EOF'
import asyncio
from backend.engine.bot_entry_engine import run_all_bots

async def main():
    print("Starting full orchestration…")
    results = await run_all_bots()
    print("Orchestration complete:", results)

asyncio.run(main())
EOF

PYTHONPATH=. python3 - << 'EOF'
from backend.engine.runner_dispatcher import dispatch_bot_by_name
from backend.engine.bot_entry_engine import BOT_BUILDERS

print("Testing orchestration for all bots…\n")
for bot in BOT_BUILDERS:
    try:
        # supply minimal defaults: ticker, contracts, days-to-exp, mode
        payload = dispatch_bot_by_name(bot, ticker="SPY", contracts=1, dte=7, mode=None)
        print(f"[OK]   {bot}: {payload}")
    except Exception as e:
        print(f"[FAIL] {bot}: {e}")
EOF

# Create a standalone orchestration tester
cat > test_orchestration.py << 'EOF'
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
EOF

# Run it
PYTHONPATH=. python3 test_orchestration.py
# 1. Fix the bad import in your metrics route
sed -i   's|^from utils.trade_logger import|get_trade_log import/(from backend.utils.trade_logger import get_trade_log)|'   backend/routes/bot_metrics_route.py
# 2. Paste & run this one-liner orchestration tester:
PYTHONPATH=. python3 - << 'EOF'
import asyncio
from backend.engine.bot_entry_engine import BOT_BUILDERS
from backend.engine.runner_dispatcher import dispatch_bot_by_name

print("▶️  Orchestrating all bots…\n")
for bot in BOT_BUILDERS:
    try:
        # supply the four required args for every build_order()
        result = dispatch_bot_by_name(bot, ticker="SPY", contracts=1, dte=7, mode=None)
        # dispatch_bot_by_name may return a coroutine if your build_order is async:
        if asyncio.iscoroutine(result):
            result = asyncio.get_event_loop().run_until_complete(result)
        print(f"[ OK ] {bot:15}: {result}")
    except Exception as e:
        print(f"[FAIL] {bot:15}: {e}")

EOF

# 1. Overwrite bot_metrics_route.py with a clean, correct import
cat > backend/routes/bot_metrics_route.py << 'EOF'
# backend/routes/bot_metrics_route.py

from fastapi import APIRouter
from backend.utils.trade_logger import get_trade_log

router = APIRouter()

@router.get("/bot_metrics/{bot_name}")
async def bot_metrics(bot_name: str):
    """
    Return the trade log for a given bot.
    """
    log = get_trade_log(bot_name)
    return {"bot": bot_name, "log": log}
EOF

# 2. Restart FastAPI so the fix takes effect
pkill -f uvicorn || true
uvicorn backend.main:app --reload &
# Give the server a moment to reload
sleep 3
# 3. Re-run the orchestration tester script
PYTHONPATH=. python3 test_orchestration.py
apply_patch << 'EOF'
*** Begin Patch
*** Update File: backend/engine/bot_entry_engine.py
@@ async def run_all_bots():
-        # adjust args as needed
-        order_payload = build_fn()  
+        # supply default parameters for orchestration
+        _defaults = {"ticker": "SPY", "contracts": 1, "dte": 7, "mode": None}
+        import asyncio as _asyncio
+        if _asyncio.iscoroutinefunction(build_fn):
+            order_payload = await build_fn(**_defaults)
+        else:
+            order_payload = build_fn(**_defaults)
*** End Patch
EOF

cd ~/skystrike_fullstack_final_release/backend/engine
patch << 'EOF'
*** Begin Patch
*** Update File: bot_entry_engine.py
@@ async def run_all_bots():
-        # adjust args as needed
-        order_payload = build_fn()
+        # supply default parameters for orchestration
+        _defaults = {"ticker": "SPY", "contracts": 1, "dte": 7, "mode": None}
+        import asyncio as _asyncio
+        if _asyncio.iscoroutinefunction(build_fn):
+            order_payload = await build_fn(**_defaults)
+        else:
+            order_payload = build_fn(**_defaults)
*** End Patch
EOF

cat << 'EOF' | patch -p1
*** Begin Patch
*** Update File: backend/engine/bot_entry_engine.py
@@ async def run_all_bots():
-        # adjust args as needed
-        order_payload = build_fn()
+        # supply default parameters for orchestration
+        _defaults = {"ticker": "SPY", "contracts": 1, "dte": 7, "mode": None}
+        import asyncio as _asyncio
+        if _asyncio.iscoroutinefunction(build_fn):
+            order_payload = await build_fn(**_defaults)
+        else:
+            order_payload = build_fn(**_defaults)
*** End Patch
EOF

cd ~/skystrike_fullstack_final_release
patch -p1 << 'EOF'
*** Begin Patch
*** Update File: backend/engine/bot_entry_engine.py
@@ async def run_all_bots():
-        # adjust args as needed
-        order_payload = build_fn()
+        # supply default parameters for orchestration
+        _defaults = {"ticker": "SPY", "contracts": 1, "dte": 7, "mode": None}
+        import asyncio as _asyncio
+        if _asyncio.iscoroutinefunction(build_fn):
+            order_payload = await build_fn(**_defaults)
+        else:
+            order_payload = build_fn(**_defaults)
*** End Patch
EOF

cd ~/skystrike_fullstack_final_release
# 1) Insert the defaults+async check in bot_entry_engine.py
sed -i "/# adjust args as needed/{
  N
  s|# adjust args as needed\n[ \t]*order_payload = build_fn()|# supply default parameters for orchestration\n        _defaults = {\"ticker\": \"SPY\", \"contracts\": 1, \"dte\": 7, \"mode\": None}\n        import asyncio as _asyncio\n        if _asyncio.iscoroutinefunction(build_fn):\n            order_payload = await build_fn(**_defaults)\n        else:\n            order_payload = build_fn(**_defaults)| 
}" backend/engine/bot_entry_engine.py
# 2) Restart uvicorn and re-run orchestration test
pkill -f uvicorn || true
uvicorn backend.main:app --reload & sleep 2
PYTHONPATH=. python3 test_orchestration.py
# 1) Patch run_all_bots() to supply defaults for ticker/contracts/dte/mode
sed -i '/# adjust args as needed/{
  N
  s|# adjust args as needed\n[[:space:]]*order_payload = build_fn()|# supply default parameters for orchestration\n            _defaults = {"ticker": "SPY", "contracts": 1, "dte": 7, "mode": None}\n            import asyncio as _asyncio\n            if _asyncio.iscoroutinefunction(build_fn):\n                order_payload = await build_fn(**_defaults)\n            else:\n                order_payload = build_fn(**_defaults)| 
}' backend/engine/bot_entry_engine.py
# 2) Restart your server and re-run orchestration test
pkill -f uvicorn || true
uvicorn backend.main:app --reload & sleep 2
PYTHONPATH=. python3 test_orchestration.py
# restart uvicorn
pkill -f uvicorn || true
uvicorn backend.main:app --reload & sleep 2
# test orchestration
PYTHONPATH=. python3 test_orchestration.py
# Restart the server
pkill -f uvicorn || true
uvicorn backend.main:app --reload & sleep 2
# Run your orchestration tester
PYTHONPATH=. python3 test_orchestration.py
# backend/engine/bot_entry_engine.py
import logging
import asyncio
logger = logging.getLogger(__name__)
# Map bot names to their build functions
BOT_BUILDERS = {
}
async def run_all_bots():
# Restart the server
pkill -f uvicorn || true
uvicorn backend.main:app --reload & sleep 2
# Run your orchestration tester
PYTHONPATH=. python3 test_orchestration.py
PYTHONPATH=. python3 backend/scripts/test_all_bots.py
PYTHONPATH=. python3 test_orchestration.py
# 1. Ensure utils is a package
touch backend/utils/__init__.py
# 2. Kill any running Uvicorn
pkill -f uvicorn
# 3. (Re)start your FastAPI app with auto-reload
uvicorn backend.main:app --reload &
# 4. In the same shell (or a new tab), set PYTHONPATH and run your orchestration test
export PYTHONPATH=.
python3 test_orchestration.py
# 1. Fix the bad import in bot_trading_routes.py
sed -i "s/auth import verify_token/from backend.utils.auth import verify_token/" backend/routes/bot_trading_routes.py
# 2. Kill any running Uvicorn instances
pkill -f uvicorn
# 3. (Re)start your FastAPI app with auto-reload in the background
uvicorn backend.main:app --reload &
# 4. Rerun the orchestration test
export PYTHONPATH=.
python3 test_orchestration.py
# 1. Add a simple verify_token stub if it’s missing
grep -q "verify_token" backend/utils/auth.py || cat << 'EOF' >> backend/utils/auth.py
from fastapi import Header, HTTPException, status

async def verify_token(authorization: str = Header(...)):
    \"\"\"
    Dummy token verification. Replace this with your JWT validation logic.
    \"\"\"
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid auth header")
    token = authorization.split(" ", 1)[1]
    # TODO: decode & verify JWT here
    return
EOF

# 2. Kill any running Uvicorn
pkill -f uvicorn
# 3. Restart FastAPI with auto-reload in the background
uvicorn backend.main:app --reload &
# 4. Re-run the orchestration test
export PYTHONPATH=.
python3 test_orchestration.py
# 1. cd into your project
cd ~/skystrike_fullstack_final_release
# 2. Create a single patch file with all three fixes
cat > fix_skystrike.patch << 'EOF'
*** Begin Patch
*** Update File: backend/utils/auth.py
@@ def verify_token(x_token: str = Header(...)):
-    \"\"\"Verify that x_token is valid and raise HTTPException if not
-    \"\"\"  # ← stray backslash before the quotes
+    """
+    Verify that x_token is valid and raise HTTPException if not
+    """

*** End Patch Part 1

*** Begin Patch
*** Update File: backend/services/tradier_client.py
@@ def get_expirations(self, ticker: str) -> list[str]:
-        data = self._request("/v1/markets/options/expirations", {"symbol": ticker})
-        return data.get("expirations", {}).get("date", [])
+        data = self._request("/v1/markets/options/expirations", {"symbol": ticker})
+        if not data or "expirations" not in data:
+            return []
+        return data["expirations"].get("date", [])

@@ def get_quote(self, ticker: str) -> dict:
-        quotes = self._request("/v1/markets/quotes", {"symbols": ticker}).get("quotes", {}).get("quote", [])
-        return quotes[0]
+        resp = self._request("/v1/markets/quotes", {"symbols": ticker})
+        quotes = resp.get("quotes", {}).get("quote", [])
+        if not quotes:
+            raise RuntimeError("No quote returned for \(ticker\)")
+        if isinstance(quotes, dict):
+            return quotes
+        return quotes[0]

*** End Patch Part 2

*** Begin Patch
*** Update File: backend/submit_order.py
@@
-    # from iron_condor is missing!
+    from backend.bots.iron_condor import build_order as ironcondor_build

@@ BUILD_MAP = {
-    # no ironcondor key
+    "ironcondor": ironcondor_build,
*** End Patch Part 3
*** End Patch
EOF

# 3. Apply the patch
patch -p0 < fix_skystrike.patch
# 4. Kill any running Uvicorn instances
pkill -f 'uvicorn backend.main:app'
# 5. Restart in reload mode (adjust as needed)
nohup uvicorn backend.main:app --reload > uvicorn.log 2>&1 &
# 6. (Optional) tail the logs to confirm startup
tail -f uvicorn.log
# 1. Go to your project root
cd ~/skystrike_fullstack_final_release
# 2. Remove the backslash in auth.py so the triple-quote is unescaped
sed -i 's/\\\"\"\"/\"\"\"/' backend/utils/auth.py
# 3. (Optional) Confirm the change
sed -n '1,20p' backend/utils/auth.py | sed -n '/def verify_token/,/"""/p'
# 4. Kill the old Uvicorn process
pkill -f 'uvicorn backend.main:app'
# 5. Restart Uvicorn in reload mode, logging to uvicorn.log
nohup uvicorn backend.main:app --reload > uvicorn.log 2>&1 &
# 6. Tail the log to watch for errors
tail -f uvicorn.log
# 1. cd into your project
cd ~/skystrike_fullstack_final_release
# 2. In the verify_token block, remove all backslashes
sed -i '/def verify_token/,/return/ s/\\//g' backend/utils/auth.py
# 3. (Quick sanity check: you should now see an unescaped triple-quote)
sed -n '/def verify_token/,/return/p' backend/utils/auth.py
# 4. Kill any running Uvicorn
pkill -f 'uvicorn backend.main:app'
# 5. Relaunch Uvicorn with reload (logging to uvicorn.log)
nohup uvicorn backend.main:app --reload > uvicorn.log 2>&1 &
# 6. Tail the log to confirm it starts cleanly
tail -f uvicorn.log
# 1. From your project root, search for any remaining backslashes in that block:
grep -n '\\\"' backend/utils/auth.py
# You should get no output. If you do see output, open the file and delete those backslashes manually:
#     nano +<line-number> backend/utils/auth.py
# 2. Quick inspect lines 1–20 around verify_token:
sed -n '1,20p' backend/utils/auth.py
# You want to see exactly:
# async def verify_token(...):
#     """
#     Dummy token verification...
#     """
#     if not authorization.startswith("Bearer "):
#         ...
# 3. Kill any existing Uvicorn:
pkill -f 'uvicorn backend.main:app'
# 4. Restart Uvicorn in the foreground (so you see errors immediately):
uvicorn backend.main:app --reload
# -- If you still see the SyntaxError, it means there's a stray backslash or non-ASCII character 
#    on line 13 of auth.py. In that case, open it with your editor and delete the backslash 
#    before the triple-quotes, then save and restart again.
# 1. Go to your project root
cd ~/skystrike_fullstack_final_release
# 2. Create a patch to fix the import in bot_trading_routes.py
cat > fix_bot_trading_routes.patch << 'EOF'
*** Begin Patch
*** Update File: backend/routes/bot_trading_routes.py
@@
-from bots import BOT_RUNNERS
+from backend.submit_order import BUILD_MAP as BOT_RUNNERS
*** End Patch
EOF

# 3. Apply the patch
patch -p0 < fix_bot_trading_routes.patch
# 4. Kill any running Uvicorn
pkill -f 'uvicorn backend.main:app'
# 5. Restart Uvicorn in the foreground to watch for errors
uvicorn backend.main:app --reload
# 1. cd into your project
cd ~/skystrike_fullstack_final_release
# 2. Fix the import in bot_trading_routes.py
sed -i 's|from bots import BOT_RUNNERS|from backend.submit_order import BUILD_MAP as BOT_RUNNERS|' backend/routes/bot_trading_routes.py
# 3. Kill any running Uvicorn
pkill -f 'uvicorn backend.main:app'
# 4. Restart Uvicorn in reload mode (foreground so you see errors)
uvicorn backend.main:app --reload
# 1. Go to your project root
cd ~/skystrike_fullstack_final_release
# 2. Remove the bad import in backend/auth.py
sed -i '/backend\.dependencies\.auth/d' backend/auth.py
# 3. Kill any running Uvicorn
pkill -f 'uvicorn backend.main:app'
# 4. Restart Uvicorn in reload mode
uvicorn backend.main:app --reload
PYTHONPATH=. python3 backend/scripts/test_all_bots.py
uvicorn backend.main:app --reload
#!/usr/bin/env bash
set -e
# Map of bad → good service module names
declare -A MAPPING=(   ["dashboard_service"]="dashboard"         # if you rename dashboard_service.py → dashboard.py
  ["dashboard"]="risk_dashboard"            # if your dashboard logic lives in risk_dashboard.py
  ["tradier_api"]="tradier_api"             # unchanged
  ["config_service"]="config_service"   ["copilot_engine"]="copilot_engine"   ["dashboard_service"]="dashboard_service" # adjust if your file is named differently
)
echo "Patching route imports to match service filenames…"
for route in backend/routes/*.py; do   for BAD in "${!MAPPING[@]}"; do     GOOD=${MAPPING[$BAD]}
    sed -i -E "s|(from \.\.services\.)${BAD}(\s+import)|\1${GOOD}\2|g" "$route";   done; done
echo "Done. Please restart Uvicorn:"
echo "  uvicorn backend.main:app --reload"
uvicorn backend.main:app --reload
# 1. Patch the dashboard_routes import
sed -i   's|from \.\./services/dashboard_service|from \.\./services/dashboard|'   backend/routes/dashboard_routes.py
# 2. (Example for broker_routes alias fix – adapt as needed)
# sed -i 's|get_positions|get_open_pnl as get_positions|' backend/routes/broker_routes.py
# 3. Restart Uvicorn to pick up your changes
uvicorn backend.main:app --reload
cat <<'EOF' > fix_imports.sh
#!/usr/bin/env bash
set -e

# Replace dashboard_service → dashboard
sed -i 's|from \.\./services/dashboard_service|from \.\./services/dashboard|' backend/routes/dashboard_routes.py

# (Add more sed lines here for other known mismatches)

echo "Imports patched. Restarting server..."
uvicorn backend.main:app --reload
EOF

chmod +x fix_imports.sh
uvicorn backend.main:app --reload
# 1) Patch the dashboard_routes import to point at services/dashboard.py
sed -i   's|from \.\./services/dashboard_service|from \.\./services/dashboard|'   backend/routes/dashboard_routes.py
# 2) (Generic template for future fixes) 
#    Replace <BAD> with the wrong module name and <GOOD> with the real filename
#    e.g. sed -i 's|from \.\./services/<BAD>|from \.\./services/<GOOD>|' <route-path>
# 3) Restart the server to pick up changes
uvicorn backend.main:app --reload
# 1) Fix the import in dashboard_routes.py
sed -i   's|from \.\./services/dashboard_service import|from ../services/dashboard import|'   backend/routes/dashboard_routes.py
# 2) Confirm the change
grep -n "services/dashboard" backend/routes/dashboard_routes.py
# 1) Fix the import in dashboard_routes.py
sed -i   's|from \.\./services/dashboard_service import|from ../services/dashboard import|'   backend/routes/dashboard_routes.py
# 2) Confirm the change
grep -n "services/dashboard" backend/routes/dashboard_routes.py
# 3) Restart Uvicorn
uvicorn backend.main:app --reload
cd ~/skystrike_fullstack_final_release/backend
uvicorn backend.main:app --reload
# Go up one level so that "backend" is a top-level package
cd ~/skystrike_fullstack_final_release
# Launch Uvicorn using the module path "backend.main:app"
uvicorn backend.main:app --reload
# From your project root or wherever you launch Uvicorn:
export TRADIER_MODE=paper       # or "live" if you have live credentials
# (If you’re using a .env file, update TRADIER_MODE in it instead.)
uvicorn backend.main:app --reload
# 1) Open backend/__init__.py and find your Settings.__init__ block
# 2) Change the validation logic from:
#       if self.TRADE_MODE not in ("paper","live"):
#           raise ValueError(...)
#    to something like:
#       if self.TRADE_MODE not in ("paper","live","sandbox"):
#           raise ValueError(...)
# 3) In the same file, add mapping for sandbox:
#       if self.TRADE_MODE == "sandbox":
#           self.TRADIER_API_KEY = os.getenv("TRADIER_SANDBOX_ACCESS_TOKEN")
#           self.ACCOUNT_ID      = os.getenv("TRADIER_SANDBOX_ACCOUNT_ID")
#       elif self.TRADE_MODE == "paper":
#           ...
#       else:  # live
#           ...
#
# 4) Save and restart:
uvicorn backend.main:app --reload
sed -i 's/^TRADIER_MODE=.*/TRADIER_MODE=paper/' .env  # or add if missing
uvicorn backend.main:app --reload
nano ~/skystrike_fullstack_final_release/backend/.env
uvicorn backend.main:app --reload
grep -rnw './backend' -e 'TRADIER_MODE'
NORMALIZE_TRADIER_MODE='
mode_raw = os.getenv("TRADIER_MODE", "sandbox").lower()
mode = "sandbox" if mode_raw in ("sandbox", "paper") else mode_raw
if mode not in ("sandbox", "live"):
    raise ValueError(f"Invalid TRADIER_MODE: {mode_raw}")
'
sed -i.bak '/TRADIER_MODE *=/{
    N;N;d
    r /dev/stdin
}' ./backend/utils/run_bot_with_params.py <<< "$NORMALIZE_TRADIER_MODE"
sed -i.bak '/TRADIER_MODE *=/{
    N;N;d
    r /dev/stdin
}' ./backend/utils/tradier_order_runner.py <<< "$NORMALIZE_TRADIER_MODE"
sed -i.bak '/TRADIER_MODE *=/{
    N;N;d
    r /dev/stdin
}' ./backend/utils/tradier_multileg.py <<< "$NORMALIZE_TRADIER_MODE"
sed -i.bak '/MODE *=/{
    N;d
    r /dev/stdin
}' ./backend/services/tradier_api.py <<< "$NORMALIZE_TRADIER_MODE"
sed -i.bak '/TRADE_MODE *=/{
    N;d
    r /dev/stdin
}' ./backend/config.py <<< "$NORMALIZE_TRADIER_MODE"
sed -i.bak '/TRADE_MODE *=/{
    N;d
    r /dev/stdin
}' ./backend/config/__init__.py <<< "$NORMALIZE_TRADIER_MODE"
sed -i.bak '/MODE *=/{
    N;d
    r /dev/stdin
}' ./backend/scripts/get_tradier_token.py <<< "$NORMALIZE_TRADIER_MODE"
grep -rnw './backend' -e 'mode_raw = os.getenv("TRADIER_MODE"'
find ./backend -name "*.bak" -delete
pkill -f uvicorn
uvicorn backend.main:app --reload
echo '
def ping_tradier() -> bool:
    """
    Lightweight ping to check Tradier API health.
    """
    try:
        resp = requests.get(f"{TRADIER_BASE_URL}/markets/clock", headers={
            "Authorization": f"Bearer {API_KEY}",
            "Accept": "application/json"
        })
        return resp.status_code == 200
    except Exception:
        return False
' >> backend/services/tradier_client.py
pkill -f uvicorn
uvicorn backend.main:app --reload
pkill -f uvicorn
uvicorn backend.main:app --reload
pkill -f 'uvicorn'
uvicorn backend.main:app --reload
portfolio
uvicorn backend.main:app --reload
nano backend/engine/final_recommendation_engine.py
pkill -f 'uvicorn'
uvicorn backend.main:app --reload
# backend/routes/dashboard_routes.py
# ❌ Remove or comment this line:
from ..services.dashboard import get_strategy_status
uvicorn backend.main:app --reload
sed -i 's|from backend.auth import get_current_user, User|from backend.utils.auth_utils import get_current_user, User|' backend/routes/bot_trigger_dynamic.py
uvicorn backend.main:app --reload
pip install fastapi "python-jose[cryptography]" pydantic
uvicorn backend.main:app --reload
sed -i 's|from backend.auth.auth_utils|from backend.utils.auth_utils|' backend/routes/order.py
pkill -f 'uvicorn'
uvicorn backend.main:app --reload
sed -i 's|from backend.bots.runner import build_order|from backend.submit_order import build_order|' backend/routes/order.py
pkill -f 'uvicorn'
uvicorn backend.main:app --reload
sed -i 's|from backend.submit_order import build_order|from backend.submit_order import BUILD_MAP|' backend/routes/order.py
uvicorn backend.main:app --reload
PYTHONPATH=. python3 backend/scripts/test_all_bots.py
find backend/bots -name "*.py" -exec sed -i 's|sandbox=(mode == "paper")|mode=mode|g' {} +
PYTHONPATH=. python3 backend/scripts/test_all_bots.py
PYTHONPATH=. python3 backend/scripts/test_all_bots.py
cd ~/skystrike_fullstack_final_release/backend
PYTHONPATH=. python3 backend/scripts/test_all_bots.py
PYTHONPATH=. python3 scripts/test_all_bots.py
cd ~/skystrike_fullstack_final_release
PYTHONPATH=. python3 backend/scripts/test_all_bots.py
nano ~/skystrike_fullstack_final_release/backend/.env
PYTHONPATH=. python3 backend/scripts/test_all_bots.py
find backend/bots -name "*.py" -exec sed -i '/def build_order.*mode.*:/a \    if mode == "paper": mode = "sandbox"' {} +
grep -rl 'mode="paper"' backend/bots | xargs sed -i 's/mode="paper"/mode="sandbox"/g'
PYTHONPATH=. python3 backend/scripts/test_all_bots.py
sed -i 's|submit_multileg_order(|submit_multileg_order(mode=mode, |g' backend/submit_order.py
sed -i 's|submit_equity_order(|submit_equity_order(mode=mode, |g' backend/submit_order.py
sed -i 's|def submit_multileg_order(|async def submit_multileg_order(\
    underlying: str, legs: List[Dict], order_type: str = "market", duration: str = "day", price: Optional[float] = None, mode: Optional[str] = None|g' backend/services/tradier_api.py
sed -i 's|def submit_equity_order(|async def submit_equity_order(\
    symbol: str, quantity: float, price: Optional[float], side: str, order_type: str = "market", duration: str = "day", mode: Optional[str] = None|g' backend/services/tradier_api.py
cat <<EOF >> backend/services/tradier_client.py

    def get_option_chain(self, symbol: str, expiration: str) -> list:
        url = f"{self.base}/markets/options/chains"
        headers = {"Authorization": f"Bearer {self.token}", "Accept": "application/json"}
        params = {"symbol": symbol, "expiration": expiration}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json().get("options", {}).get("option", [])
EOF

sed -i 's|def __init__(self, token: Optional.*)|def __init__(self, token: Optional[str] = None, account_id: Optional[str] = None, mode: Optional[str] = None):|g' backend/services/tradier_client.py
sed -i '/def __init__/a \ \ \ \ mode = (mode or os.getenv("TRADIER_MODE", "sandbox")).lower()\n        if mode not in ("sandbox", "live"): raise ValueError(f"Invalid TRADIER_MODE: {mode}")\n        self.base = LIVE_BASE if mode == "live" else SANDBOX_BASE\n        self.token = token or (os.getenv("TRADIER_LIVE_ACCESS_TOKEN") if mode == "live" else os.getenv("TRADIER_SANDBOX_ACCESS_TOKEN"))\n        self.account_id = account_id or (os.getenv("TRADIER_LIVE_ACCOUNT_ID") if mode == "live" else os.getenv("TRADIER_SANDBOX_ACCOUNT_ID"))' backend/services/tradier_client.py
pkill -f uvicorn
uvicorn backend.main:app --reload
PYTHONPATH=. python3 backend/scripts/test_all_bots.py
# View the problem line:
grep "submit_multileg_order" backend/submit_order.py
# Then fix manually in your editor OR run:
sed -i 's/mode=mode, *mode=mode/mode=mode/' backend/submit_order.py
uvicorn backend.main:app --reload
PYTHONPATH=. python3 backend/scripts/test_all_bots.py
# Check where the bad line is:
grep 'se\$f' backend/services/tradier_client.py
# Then open the file:
nano backend/services/tradier_client.py
# Search (`Ctrl + W`) for: se$f
# Fix the line to the correct Python syntax:
# raise ValueError(f"Invalid TRADIER_MODE: {mode}")
# Save and exit (`Ctrl + O`, Enter, then `Ctrl + X`)
PYTHONPATH=. python3 backend/scripts/test_all_bots.py
nano ~/skystrike_fullstack_final_release/backend/.env
PYTHONPATH=. python3 backend/scripts/test_all_bots.py
echo 'import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))
' | cat - backend/scripts/test_all_bots.py > backend/scripts/test_all_bots_patched.py && mv backend/scripts/test_all_bots_patched.py backend/scripts/test_all_bots.py
PYTHONPATH=. python3 backend/scripts/test_all_bots.py
sed -i 's|from backend.services.tradier_api import (|from backend.services.tradier_client import (|' backend/submit_order.py
PYTHONPATH=. python3 backend/scripts/test_all_bots.py
sed -i '/from backend.services.tradier_client import/d' backend/submit_order.py && sed -i '6i from backend.services.option_lookup import get_tradier_option_symbol\nfrom backend.services.tradier_client import TradierClient' backend/submit_order.py
PYTHONPATH=. python3 backend/scripts/test_all_bots.py
sed -i '/submit_multileg_order/d' backend/submit_order.py && sed -i '/submit_equity_order/d' backend/submit_order.py && sed -i '/from backend.services.tradier_client import/d' backend/submit_order.py && sed -i '6i from backend.services.option_lookup import get_tradier_option_symbol\nfrom backend.services.tradier_client import TradierClient' backend/submit_order.py
PYTHONPATH=. python3 backend/scripts/test_all_bots.py
sed -i '/from backend.services.tradier_client import/,/)/d' backend/submit_order.py && sed -i '6i from backend.services.tradier_client import TradierClient\nfrom backend.services.option_lookup import get_tradier_option_symbol' backend/submit_order.py
sed -i '/from backend.services.tradier_client import/,/)/d' backend/submit_order.py && sed -i '6i from backend.services.tradier_client import TradierClient\nfrom backend.services.option_lookup import get_tradier_option_symbol' backend/submit_order.py
PYTHONPATH=. python3 backend/scripts/test_all_bots.py
sed -i '/from backend.services.tradier_client import/,/)/d' backend/submit_order.py && sed -i '/from backend.services.option_lookup import/d' backend/submit_order.py && sed -i '6i from backend.services.tradier_client import TradierClient\nfrom backend.services.option_lookup import get_tradier_option_symbol' backend/submit_order.py
PYTHONPATH=. python3 backend/scripts/test_all_bots.py
PYTHONPATH=. python3 backend/scripts/test_all_bots.py
cd ~/skystrike_fullstack_final_release/backend
PYTHONPATH=. python3 backend/scripts/test_all_bots.py
PYTHONPATH=. python3 scripts/test_all_bots.py
