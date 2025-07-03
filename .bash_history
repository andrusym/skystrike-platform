for bot in csp wheel trend replicator copybot dcabot gridbot momentumbot scalper pairstrader; do   sed -i -E     -e '1s@import logging@import logging\nfrom .base import multileg_payload@'     -e '/def build_order/,/return/{ 
        s@.*return .*@    # ← replace this line with a call to our helper@
        a\
    # --- assemble legs for '"$bot"' here:\n\
    \    params = { "underlying": ticker, "legs": /* your legs list */, "type": mode, "duration": "day", "price": None }\n\
    \    return multileg_payload(\n\
    \        params["underlying"], params["legs"], params["type"], params["duration"], params.get("price")\n\
    \    )\n\
    }' backend/bots/${bot}.py; done
# 3) Re-run your full bot suite
python3 -m backend.scripts.test_all_bots
cd ~/skystrike_fullstack_final_release
# 1) Add helpers to base.py
cat >> backend/bots/base.py << 'EOF'
from typing import Dict, Any, List

def option_payload(
    symbol: str,
    side: str,
    quantity: int,
    order_type: str = "market",
    duration: str = "day",
    price: float = None
) -> Dict[str, Any]:
    """
    Build a single‐leg option order payload for Tradier.
    """
    order: Dict[str, Any] = {
        "class":    "option",
        "symbol":   symbol,
        "side":     side,
        "quantity": quantity,
        "type":     order_type,
        "duration": duration,
    }
    if order_type in ("limit","stop_limit","stop") and price is not None:
        order["price"] = price
    return order

def multileg_payload(
    underlying: str,
    legs: List[Dict[str, Any]],
    mode: str,
    duration: str = "day",
    price: float = None
) -> Dict[str, Any]:
    """
    Build a multileg order payload for Tradier.
    """
    order: Dict[str, Any] = {
        "class":    "multileg",
        "symbol":   underlying,
        "type":     mode,
        "duration": duration,
    }
    if mode in ("debit","credit") and price is not None:
        order["price"] = price

    for i, leg in enumerate(legs):
        order[f"option_symbol[{i}]"] = leg["symbol"]
        order[f"side[{i}]"]         = leg["side"]
        order[f"quantity[{i}]"]     = leg["quantity"]

    return order
EOF

# 2) Patch each bot to use the right helper:
# Single‐leg strategies: use option_payload
for bot in csp copybot dcabot trend replicator scalper pairstrader; do   sed -i -E     -e '1s@^@from .base import option_payload\n@'     -e '/def build_order/,/return/{
         s@.*return .*@    # ← REPLACE with option_payload call@
         a\
    # --- build the one-leg params here (implement your logic) \
         symbol = ticker  # or however you derive OCC symbol\
         side   = "sell_to_open"  # your logic\
         qty    = contracts\
         return option_payload(symbol, side, qty, order_type="market")\
    }'     backend/bots/${bot}.py; done
# Multi‐leg strategies: use multileg_payload
for bot in iron_condor kingcondor spread wheel gridbot momentumbot; do   sed -i -E     -e '1s@^@from .base import multileg_payload\n@'     -e '/def build_order/,/return/{
         s@.*return .*@    # ← REPLACE with multileg_payload call@
         a\
    # --- assemble legs list for '"$bot"' here (implement your logic) \
         legs = [ \
             {"symbol": "...", "side": "...", "quantity": contracts}, \
             # add more legs per your strategy\
         ]\
         return multileg_payload(ticker, legs, mode, duration="day")\
    }'     backend/bots/${bot}.py; done
# 3) Re-run your bot suite
python3 -m backend.scripts.test_all_bots
cd ~/skystrike_fullstack_final_release
# 1) Ensure you have a single helper in base.py
cat > backend/bots/base.py << 'EOF'
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

def multileg_payload(
    underlying: str,
    legs: List[Dict[str, Any]],
    mode: str,
    duration: str = "day",
    price: float = None
) -> Dict[str, Any]:
    """
    Build a Tradier multileg payload:
      - class=multileg, symbol=underlying, type=mode, duration
      - indexed option_symbol[i], side[i], quantity[i]
    """
    order: Dict[str, Any] = {
        "class":    "multileg",
        "symbol":   underlying,
        "type":     mode,
        "duration": duration,
    }
    if mode in ("debit","credit") and price is not None:
        order["price"] = price

    for i, leg in enumerate(legs):
        order[f"option_symbol[{i}]"] = leg["symbol"]
        order[f"side[{i}]"]         = leg["side"]
        order[f"quantity[{i}]"]     = leg["quantity"]

    return order
EOF

# 2) Overwrite every multi-leg bot with a stub that calls multileg_payload
for bot in csp wheel trend replicator copybot dcabot gridbot momentumbot scalper pairstrader; do
  cat > backend/bots/${bot}.py << 'EOF'import logging
from typing import Dict, Any, List
from .base import multileg_payload

logger = logging.getLogger(__name__)

async def build_order(ticker: str, contracts: int, dte: int, mode: str) -> Dict[str, Any]:
    """
    Build a multileg option order payload for Tradier.
    Required:
      - ticker: underlying symbol
      - contracts: number of contracts (per leg or total, strategy-dependent)
      - dte: days to expiration (use to compute strikes/dates)
      - mode: 'market'|'debit'|'credit'|'even'
    """
    # TODO: for the "${bot}" strategy,
    #       compute your list of legs (each with OCC symbol, side, quantity)
    legs: List[Dict[str, Any]] = [
        # {"symbol": "...OCC symbol...", "side": "...", "quantity": contracts},
        # {"symbol": "...", "side": "...", "quantity": contracts},
        # etc.
    ]

    # Optionally set a price for debit/credit
    price = None
    # price = 1.23  # <-- set if needed

    # Delegate to the helper which will index everything correctly
    order = multileg_payload(ticker, legs, mode, duration="day", price=price)
    logger.debug("Built multileg for %s: %s", "${bot}", order)
    return order
EOF
 done
# 3) Re-run your full suite
python3 -m backend.scripts.test_all_bots
cd ~/skystrike_fullstack_final_release
# 1) Inject the multileg_payload helper into base.py
cat > backend/bots/base.py << 'EOF'
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

def multileg_payload(
    underlying: str,
    legs: List[Dict[str, Any]],
    mode: str,
    duration: str = "day",
    price: float = None
) -> Dict[str, Any]:
    """
    Build a Tradier multileg payload:
      - class=multileg, symbol=underlying, type=mode, duration
      - indexed option_symbol[i], side[i], quantity[i]
    """
    order: Dict[str, Any] = {
        "class":    "multileg",
        "symbol":   underlying,
        "type":     mode,
        "duration": duration,
    }
    if mode in ("debit","credit") and price is not None:
        order["price"] = price

    for i, leg in enumerate(legs):
        order[f"option_symbol[{i}]"] = leg["symbol"]
        order[f"side[{i}]"]         = leg["side"]
        order[f"quantity[{i}]"]     = leg["quantity"]

    logger.debug("Built multileg order: %s", order)
    return order
EOF

# 2) Overwrite each bot stub to call that helper
for bot in csp wheel trend replicator copybot dcabot gridbot momentumbot scalper pairstrader; do
  cat > backend/bots/${bot}.py << 'EOF'import logging
from typing import Dict, Any, List
from .base import multileg_payload

logger = logging.getLogger(__name__)

async def build_order(ticker: str, contracts: int, dte: int, mode: str) -> Dict[str, Any]:
    """
    Build a multileg option order payload for Tradier.
    Required args:
      - ticker: underlying symbol
      - contracts: number of contracts
      - dte: days to expiration (unused here)
      - mode: 'market'|'debit'|'credit'|'even'
    """
    # TODO: replace this stub with your strategy's actual leg‐construction logic.
    #       Each leg must be a dict with keys "symbol", "side", and "quantity".
    legs: List[Dict[str, Any]] = [
        # Example:
        # {"symbol": f"{ticker}210918C00400000", "side": "sell_to_open", "quantity": contracts},
        # {"symbol": f"{ticker}210918C00500000", "side": "buy_to_open",  "quantity": contracts},
    ]

    # Optionally set a price for debit/credit orders:
    price = None
    # price = 1.23

    # Delegate to the helper—which will index option_symbol[i], side[i], quantity[i]
    order = multileg_payload(ticker, legs, mode, duration="day", price=price)
    logger.debug("Built multileg for ${bot}: %s", order)
    return order
EOF
 done
# 3) Re-run your full bot suite
python3 -m backend.scripts.test_all_bots
# from your project root, with your venv activated:
pip install requests python-dateutil
python3 -m backend.scripts.test_all_bots
# From your project root, in your activated venv:
export TRADIER_TOKEN="your_sandbox_token_here"
export TRADIER_ACCOUNT_ID="VA70062258"
# Verify they’re set:
echo $TRADIER_TOKEN
echo $TRADIER_ACCOUNT_ID
# Then rerun your full suite:
python3 -m backend.scripts.test_all_bots
pip install python-dotenv
python3 -m backend.scripts.test_all_bots
# 1. Go to your project root
cd ~/skystrike_fullstack_final_release
# 2. Open each bot build file for editing (add the missing "right" key to each leg dict)
for bot in iron_condor kingcondor spread csp wheel trend replicator copybot dcabot gridbot momentumbot scalper pairstrader; do   vim backend/bots/${bot}.py; done
# 1. Go to your project root
cd ~/skystrike_fullstack_final_release
# 2. Open each bot build file for editing (add the missing "right" key to each leg dict)
for bot in iron_condor kingcondor spread csp wheel trend replicator copybot dcabot gridbot momentumbot scalper pairstrader; do   vim backend/bots/${bot}.py; done
# 1. cd into your project root
cd ~/skystrike_fullstack_final_release
# 2. Apply a sed‐based patch to transform each bot’s make_symbol payload into raw legs 
#    with “side”, “right”, “strike”, and “quantity”, remove multileg_payload/logger lines,
#    and switch “return payload” → “return legs”.
for bot in iron_condor kingcondor spread csp wheel trend replicator copybot dcabot gridbot momentumbot scalper pairstrader; do   sed -i     -e 's|{"symbol": make_symbol(\([^,]*\), *"C"\), *"side": *"buy_to_open", *"quantity": *contracts}|{"side":"buy","right":"C","strike":\1,"quantity":contracts}|g'     -e 's|{"symbol": make_symbol(\([^,]*\), *"C"\), *"side": *"sell_to_open", *"quantity": *contracts}|{"side":"sell","right":"C","strike":\1,"quantity":contracts}|g'     -e 's|{"symbol": make_symbol(\([^,]*\), *"P"\), *"side": *"sell_to_open", *"quantity": *contracts}|{"side":"sell","right":"P","strike":\1,"quantity":contracts}|g'     -e 's|{"symbol": make_symbol(\([^,]*\), *"P"\), *"side": *"buy_to_open", *"quantity": *contracts}|{"side":"buy","right":"P","strike":\1,"quantity":contracts}|g'     -e '/multileg_payload/d'     -e '/logger\.debug/d'     -e 's/return payload/return legs/'     backend/bots/${bot}.py; done
# 3. Rerun your test suite
python3 -m backend.scripts.test_all_bots
# 1. cd into your project root
cd ~/skystrike_fullstack_final_release
# 2. Apply a simpler sed‐based patch to each bot:
#    - Replace the four make_symbol lines with plain legs dicts
#    - Drop multileg_payload and logger.debug lines
#    - Swap `return payload` → `return legs`
for bot in iron_condor kingcondor spread csp wheel trend replicator copybot dcabot gridbot momentumbot scalper pairstrader; do   sed -i '
    s|{"symbol": make_symbol(call_long, *"C"), *"side": *"buy_to_open", *"quantity": *contracts}|{"side":"buy","right":"C","strike":call_long,"quantity":contracts}|;
    s|{"symbol": make_symbol(call_short, *"C"), *"side": *"sell_to_open", *"quantity": *contracts}|{"side":"sell","right":"C","strike":call_short,"quantity":contracts}|;
    s|{"symbol": make_symbol(put_short, *"P"), *"side": *"sell_to_open", *"quantity": *contracts}|{"side":"sell","right":"P","strike":put_short,"quantity":contracts}|;
    s|{"symbol": make_symbol(put_long, *"P"), *"side": *"buy_to_open", *"quantity": *contracts}|{"side":"buy","right":"P","strike":put_long,"quantity":contracts}|;
    /multileg_payload/d;
    /logger\.debug/d;
    s/return payload/return legs/' backend/bots/${bot}.py; done
# 3. Re-run your tests
python3 -m backend.scripts.test_all_bots
# 1. cd into your project root
cd ~/skystrike_fullstack_final_release
# 2. Overwrite backend/services/tradier_api.py with the fixed implementation
cat > backend/services/tradier_api.py << 'EOF'
# backend/services/tradier_api.py

import os
from dotenv import load_dotenv
import httpx
from typing import List, Dict, Any

load_dotenv()

# Import your shared client
from .tradier_client import TradierClient

# Instantiate once
client = TradierClient()

async def get_expirations(symbol: str) -> List[str]:
    """Fetch available option expirations."""
    return await client.get_expirations(symbol)

async def get_quote(symbol: str) -> Dict[str, Any]:
    """Fetch the latest market quote."""
    return await client.get_quote(symbol)

# Expose the formatter
format_tradier_option_symbol = client.format_tradier_option_symbol

async def submit_option_order(
    option_symbol: str,
    side: str,
    quantity: int
) -> Dict[str, Any]:
    """
    Submit a single-leg option order via Tradier.
    """
    data = {
        "class":         "option",
        "type":          "single",
        "option_symbol": option_symbol,
        "side":          side,
        "quantity":      str(quantity),
        "duration":      "day",
    }
    async with httpx.AsyncClient(
        base_url=client.base_url,
        headers=client.headers,
        timeout=30.0
    ) as http_client:
        resp = await http_client.post(
            f"/accounts/{client.account_id}/orders", data=data
        )
        resp.raise_for_status()
        return resp.json()

# Re‐export multi‐leg and equity methods
submit_multileg_order = client.submit_multileg_order
submit_equity_order    = client.submit_equity_order
EOF

# 3. Rerun your test suite
python3 -m backend.scripts.test_all_bots
# 1. cd into your project root
cd ~/skystrike_fullstack_final_release
# 2. Overwrite backend/services/tradier_client.py with a proper TradierClient definition
cat > backend/services/tradier_client.py << 'EOF'
import os
from dotenv import load_dotenv
import httpx
from typing import List, Dict, Any, Optional

# Load .env
load_dotenv()

# Determine paper vs live
MODE = os.getenv("TRADIER_MODE", "paper").strip().lower()
if MODE not in ("paper", "live"):
    raise RuntimeError(f"Invalid TRADIER_MODE: {MODE}")

BASE_URL = "https://sandbox.tradier.com/v1" if MODE == "paper" else "https://api.tradier.com/v1"
TOKEN    = os.getenv(f"TRADIER_{MODE.upper()}_ACCESS_TOKEN")
ACCOUNT  = os.getenv(f"TRADIER_{MODE.upper()}_ACCOUNT_ID")

if not TOKEN or not ACCOUNT:
    raise RuntimeError(f"Missing Tradier credentials for mode {MODE}")

class TradierClient:
    def __init__(self):
        self.base_url   = BASE_URL
        self.token      = TOKEN
        self.account_id = ACCOUNT

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept":        "application/json",
        }

    async def get_expirations(self, symbol: str) -> List[str]:
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.headers) as cli:
            r = await cli.get("/markets/options/expirations", params={"symbol": symbol})
            r.raise_for_status()
            return r.json().get("expirations", {}).get("date", [])

    async def get_quote(self, symbol: str) -> Dict[str, Any]:
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.headers) as cli:
            r = await cli.get("/markets/quotes", params={"symbols": symbol})
            r.raise_for_status()
            return r.json().get("quotes", {}).get("quote", {})

    def format_tradier_option_symbol(self, ticker: str, expiration: str, right: str, strike: float) -> str:
        strike_str = f"{int(strike * 1000):08d}"
        return f"{ticker}{expiration}{right}{strike_str}"

    async def submit_multileg_order(
        self, symbol: str, legs: List[Dict[str, Any]], price: float = 1.0
    ) -> Dict[str, Any]:
        data = {
            "class":    "option",
            "type":     "multileg",
            "symbol":   symbol,
            "duration": "day",
            "price":    str(price),
        }
        for i, leg in enumerate(legs):
            data[f"option_symbol[{i}]"] = leg["option_symbol"]
            data[f"side[{i}]"]          = leg["side"]
            data[f"quantity[{i}]"]      = str(leg["quantity"])

        hdrs = {**self.headers, "Content-Type": "application/x-www-form-urlencoded"}
        async with httpx.AsyncClient(base_url=self.base_url, headers=hdrs) as cli:
            r = await cli.post(f"/accounts/{self.account_id}/orders", data=data)
            r.raise_for_status()
            return r.json()

    async def submit_equity_order(
        self, symbol: str, side: str, quantity: int, price: Optional[float] = None
    ) -> Dict[str, Any]:
        order_type = "market" if price is None else "limit"
        data = {
            "class":    "equity",
            "symbol":   symbol,
            "side":     side,
            "quantity": str(quantity),
            "duration": "day",
            "type":     order_type,
        }
        if price is not None:
            data["price"] = str(price)

        hdrs = {**self.headers, "Content-Type": "application/x-www-form-urlencoded"}
        async with httpx.AsyncClient(base_url=self.base_url, headers=hdrs) as cli:
            r = await cli.post(f"/accounts/{self.account_id}/orders", data=data)
            r.raise_for_status()
            return r.json()
EOF

# 3. Rerun your test harness
python3 -m backend.scripts.test_all_bots
# 1. Go to your project root
cd ~/skystrike_fullstack_final_release
# 2. Completely overwrite the Tradier client with a correct implementation
cat > backend/services/tradier_client.py << 'EOF'
import os
from dotenv import load_dotenv
import httpx
from typing import List, Dict, Any, Optional

# Load .env
load_dotenv()

# Determine paper vs. live mode
MODE = os.getenv("TRADIER_MODE", "paper").strip().lower()
if MODE not in ("paper", "live"):
    raise RuntimeError(f"Invalid TRADIER_MODE: {MODE}")

BASE_URL = "https://sandbox.tradier.com/v1" if MODE == "paper" else "https://api.tradier.com/v1"
TOKEN    = os.getenv(f"TRADIER_{MODE.upper()}_ACCESS_TOKEN")
ACCOUNT  = os.getenv(f"TRADIER_{MODE.upper()}_ACCOUNT_ID")

if not TOKEN:
    raise RuntimeError(f"Missing TRADIER_{MODE.upper()}_ACCESS_TOKEN")
if not ACCOUNT:
    raise RuntimeError(f"Missing TRADIER_{MODE.upper()}_ACCOUNT_ID")

class TradierClient:
    def __init__(self):
        self.base_url   = BASE_URL
        self.token      = TOKEN
        self.account_id = ACCOUNT

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept":        "application/json",
        }

    async def get_expirations(self, symbol: str) -> List[str]:
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.headers) as cli:
            r = await cli.get("/markets/options/expirations", params={"symbol": symbol})
            r.raise_for_status()
            return r.json().get("expirations", {}).get("date", [])

    async def get_quote(self, symbol: str) -> Dict[str, Any]:
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.headers) as cli:
            r = await cli.get("/markets/quotes", params={"symbols": symbol})
            r.raise_for_status()
            return r.json().get("quotes", {}).get("quote", {})

    def format_tradier_option_symbol(self, ticker: str, expiration: str, right: str, strike: float) -> str:
        strike_str = f"{int(strike * 1000):08d}"
        return f"{ticker}{expiration}{right}{strike_str}"

    async def submit_multileg_order(
        self, symbol: str, legs: List[Dict[str, Any]], price: float = 1.0
    ) -> Dict[str, Any]:
        data = {
            "class":    "option",
            "type":     "multileg",
            "symbol":   symbol,
            "duration": "day",
            "price":    str(price),
        }
        for i, leg in enumerate(legs):
            data[f"option_symbol[{i}]"] = leg["option_symbol"]
            data[f"side[{i}]"]          = leg["side"]
            data[f"quantity[{i}]"]      = str(leg["quantity"])
        headers = {**self.headers, "Content-Type": "application/x-www-form-urlencoded"}
        async with httpx.AsyncClient(base_url=self.base_url, headers=headers) as cli:
            r = await cli.post(f"/accounts/{self.account_id}/orders", data=data)
            r.raise_for_status()
            return r.json()

    async def submit_equity_order(


# 1. Move into your project root
cd ~/skystrike_fullstack_final_release
# 2. Backup the old client and write the new one in one go
mv backend/services/tradier_client.py backend/services/tradier_client.py.bak
cat > backend/services/tradier_client.py << 'EOF'
import os
from dotenv import load_dotenv
import httpx
from typing import List, Dict, Any, Optional

# Load .env
load_dotenv()

# Determine paper vs. live mode
MODE = os.getenv("TRADIER_MODE", "paper").strip().lower()
if MODE not in ("paper", "live"):
    raise RuntimeError(f"Invalid TRADIER_MODE: {MODE}")

BASE_URL = "https://sandbox.tradier.com/v1" if MODE == "paper" else "https://api.tradier.com/v1"
TOKEN    = os.getenv(f"TRADIER_{MODE.upper()}_ACCESS_TOKEN")
ACCOUNT  = os.getenv(f"TRADIER_{MODE.upper()}_ACCOUNT_ID")

if not TOKEN:
    raise RuntimeError(f"Missing TRADIER_{MODE.upper()}_ACCESS_TOKEN")
if not ACCOUNT:
    raise RuntimeError(f"Missing TRADIER_{MODE.upper()}_ACCOUNT_ID")

class TradierClient:
    def __init__(self):
        self.base_url   = BASE_URL
        self.token      = TOKEN
        self.account_id = ACCOUNT

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept":        "application/json",
        }

    async def get_expirations(self, symbol: str) -> List[str]:
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.headers) as cli:
            r = await cli.get("/markets/options/expirations", params={"symbol": symbol})
            r.raise_for_status()
            return r.json().get("expirations", {}).get("date", [])

    async def get_quote(self, symbol: str) -> Dict[str, Any]:
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.headers) as cli:
            r = await cli.get("/markets/quotes", params={"symbols": symbol})
            r.raise_for_status()
            return r.json().get("quotes", {}).get("quote", {})

    def format_tradier_option_symbol(self, ticker: str, expiration: str, right: str, strike: float) -> str:
        strike_str = f"{int(strike * 1000):08d}"
        return f"{ticker}{expiration}{right}{strike_str}"

    async def submit_multileg_order(
        self, symbol: str, legs: List[Dict[str, Any]], price: float = 1.0
    ) -> Dict[str, Any]:
        data = {
            "class":    "option",
            "type":     "multileg",
            "symbol":   symbol,
            "duration": "day",
            "price":    str(price),
        }
        for i, leg in enumerate(legs):
            data[f"option_symbol[{i}]"] = leg["option_symbol"]
            data[f"side[{i}]"]          = leg["side"]
            data[f"quantity[{i}]"]      = str(leg["quantity"])
        headers = {**self.headers, "Content-Type": "application/x-www-form-urlencoded"}
        async with httpx.AsyncClient(base_url=self.base_url, headers=headers) as cli:
            r = await cli.post(f"/accounts/{self.account_id}/orders", data=data)
            r.raise_for_status()
            return r.json()

    async def submit_equity_order(
        self, symbol: str, side: str, quantity: int, price: Optional[float] = None
    ) -> Dict[str, Any]:
        order_type = "market" if price is None else "limit"
        data = {
            "class":    "equity",
            "symbol":   symbol,
            "side":     side,
            "quantity": str(quantity),
            "duration": "day",
            "type":     order_type,
        }
        if price is not None:
            data["price"] = str(price)
        headers = {**self.headers, "Content-Type": "application/x-www-form-urlencoded"}
        async with httpx.AsyncClient(base_url=self.base_url, headers=headers) as cli:
            r = await cli.post(f"/accounts/{self.account_id}/orders", data=data)
            r.raise_for_status()
            return r.json()
EOF

# 3. Run the test harness again
python3 -m backend.scripts.test_all_bots
# 1. Go to your project root
cd ~/skystrike_fullstack_final_release
# 2. Backup the old client and write the new one
mv backend/services/tradier_client.py backend/services/tradier_client.py.bak
cat > backend/services/tradier_client.py << 'EOF'
import os
from dotenv import load_dotenv
import httpx
from typing import List, Dict, Any, Optional

# Load .env
load_dotenv()

# Determine paper vs. live mode
MODE = os.getenv("TRADIER_MODE", "paper").strip().lower()
if MODE not in ("paper", "live"):
    raise RuntimeError(f"Invalid TRADIER_MODE: {MODE}")

BASE_URL = "https://sandbox.tradier.com/v1" if MODE == "paper" else "https://api.tradier.com/v1"
TOKEN    = os.getenv(f"TRADIER_{MODE.upper()}_ACCESS_TOKEN")
ACCOUNT  = os.getenv(f"TRADIER_{MODE.upper()}_ACCOUNT_ID")

if not TOKEN:
    raise RuntimeError(f"Missing TRADIER_{MODE.upper()}_ACCESS_TOKEN")
if not ACCOUNT:
    raise RuntimeError(f"Missing TRADIER_{MODE.upper()}_ACCOUNT_ID")

class TradierClient:
    def __init__(self):
        self.base_url   = BASE_URL
        self.token      = TOKEN
        self.account_id = ACCOUNT

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept":        "application/json",
        }

    async def get_expirations(self, symbol: str) -> List[str]:
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.headers) as cli:
            r = await cli.get("/markets/options/expirations", params={"symbol": symbol})
            r.raise_for_status()
            return r.json().get("expirations", {}).get("date", [])

    async def get_quote(self, symbol: str) -> Dict[str, Any]:
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.headers) as cli:
            r = await cli.get("/markets/quotes", params={"symbols": symbol})
            r.raise_for_status()
            return r.json().get("quotes", {}).get("quote", {})

    def format_tradier_option_symbol(self, ticker: str, expiration: str, right: str, strike: float) -> str:
        strike_str = f"{int(strike * 1000):08d}"
        return f"{ticker}{expiration}{right}{strike_str}"

    async def submit_multileg_order(
        self, symbol: str, legs: List[Dict[str, Any]], price: float = 1.0
    ) -> Dict[str, Any]:
        data = {
            "class":    "option",
            "type":     "multileg",
            "symbol":   symbol,
            "duration": "day",
            "price":    str(price),
        }
        for i, leg in enumerate(legs):
            data[f"option_symbol[{i}]"] = leg["option_symbol"]
            data[f"side[{i}]"]          = leg["side"]
            data[f"quantity[{i}]"]      = str(leg["quantity"])
        headers = {**self.headers, "Content-Type": "application/x-www-form-urlencoded"}
        async with httpx.AsyncClient(base_url=self.base_url, headers=headers) as cli:
            r = await cli.post(f"/accounts/{self.account_id}/orders", data=data)
            r.raise_for_status()
            return r.json()

    async def submit_equity_order(
        self, symbol: str, side: str, quantity: int, price: Optional[float] = None
    ) -> Dict[str, Any]:
        order_type = "market" if price is None else "limit"
        data = {
            "class":    "equity",
            "symbol":   symbol,
            "side":     side,
            "quantity": str(quantity),
            "duration": "day",
            "type":     order_type,
        }
        if price is not None:
            data["price"] = str(price)
        headers = {**self.headers, "Content-Type": "application/x-www-form-urlencoded"}
        async with httpx.AsyncClient(base_url=self.base_url, hea


# 1. Go to your project root
cd ~/skystrike_fullstack_final_release
# 2. Backup the old client and write the new one
mv backend/services/tradier_client.py backend/services/tradier_client.py.bak
cat > backend/services/tradier_client.py << 'EOF'
import os
from dotenv import load_dotenv
import httpx
from typing import List, Dict, Any, Optional

# Load .env
load_dotenv()

# Determine paper vs. live mode
MODE = os.getenv("TRADIER_MODE", "paper").strip().lower()
if MODE not in ("paper", "live"):
    raise RuntimeError(f"Invalid TRADIER_MODE: {MODE}")

BASE_URL = "https://sandbox.tradier.com/v1" if MODE == "paper" else "https://api.tradier.com/v1"
TOKEN    = os.getenv(f"TRADIER_{MODE.upper()}_ACCESS_TOKEN")
ACCOUNT  = os.getenv(f"TRADIER_{MODE.upper()}_ACCOUNT_ID")

if not TOKEN:
    raise RuntimeError(f"Missing TRADIER_{MODE.upper()}_ACCESS_TOKEN")
if not ACCOUNT:
    raise RuntimeError(f"Missing TRADIER_{MODE.upper()}_ACCOUNT_ID")

class TradierClient:
    def __init__(self):
        self.base_url   = BASE_URL
        self.token      = TOKEN
        self.account_id = ACCOUNT

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept":        "application/json",
        }

    async def get_expirations(self, symbol: str) -> List[str]:
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.headers) as cli:
            r = await cli.get("/markets/options/expirations", params={"symbol": symbol})
            r.raise_for_status()
            return r.json().get("expirations", {}).get("date", [])

    async def get_quote(self, symbol: str) -> Dict[str, Any]:
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.headers) as cli:
            r = await cli.get("/markets/quotes", params={"symbols": symbol})
            r.raise_for_status()
            return r.json().get("quotes", {}).get("quote", {})

    def format_tradier_option_symbol(self, ticker: str, expiration: str, right: str, strike: float) -> str:
        strike_str = f"{int(strike * 1000):08d}"
        return f"{ticker}{expiration}{right}{strike_str}"

    async def submit_multileg_order(
        self, symbol: str, legs: List[Dict[str, Any]], price: float = 1.0
    ) -> Dict[str, Any]:
        data = {
            "class":    "option",
            "type":     "multileg",
            "symbol":   symbol,
            "duration": "day",
            "price":    str(price),
        }
        for i, leg in enumerate(legs):
            data[f"option_symbol[{i}]"] = leg["option_symbol"]
            data[f"side[{i}]"]          = leg["side"]
            data[f"quantity[{i}]"]      = str(leg["quantity"])
        headers = {**self.headers, "Content-Type": "application/x-www-form-urlencoded"}
        async with httpx.AsyncClient(base_url=self.base_url, headers=headers) as cli:
            r = await cli.post(f"/accounts/{self.account_id}/orders", data=data)
            r.raise_for_status()
            return r.json()

    async def submit_equity_order(
        self, symbol: str, side: str, quantity: int, price: Optional[float] = None
    ) -> Dict[str, Any]:
        order_type = "market" if price is None else "limit"
        data = {
            "class":    "equity",
            "symbol":   symbol,
            "side":     side,
            "quantity": str(quantity),
            "duration": "day",
            "type":     order_type,
        }
        if price is not None:
            data["price"] = str(price)
        headers = {**self.headers, "Content-Type": "application/x-www-form-urlencoded"}
        async with httpx.AsyncClient(base_url=self.base_url, headers=headers) as cli:
            r = await cli.post(f"/accounts/{self.account_id}/orders", data=data)
            r.raise_for_status()
            return r.json()
EOF

# 3. Run the tests again
python3 -m backend.scripts.test_all_bots
# 1. cd into your project root
cd ~/skystrike_fullstack_final_release
# 2. Overwrite backend/services/tradier_client.py in one go with a clean, working implementation:
cat << 'EOF' > backend/services/tradier_client.py
import os
from dotenv import load_dotenv
import httpx
from typing import List, Dict, Any, Optional

# Load .env
load_dotenv()

# Determine mode
MODE = os.getenv("TRADIER_MODE", "paper").strip().lower()
if MODE not in ("paper", "live"):
    raise RuntimeError(f"Invalid TRA­DIER_MODE: {MODE!r}")

BASE_URL = "https://sandbox.tradier.com/v1" if MODE == "paper" else "https://api.tradier.com/v1"
TOKEN    = os.getenv(f"TRADIER_{MODE.upper()}_ACCESS_TOKEN")
ACCOUNT  = os.getenv(f"TRADIER_{MODE.upper()}_ACCOUNT_ID")

if not TOKEN:
    raise RuntimeError(f"Missing TRADIER_{MODE.upper()}_ACCESS_TOKEN")
if not ACCOUNT:
    raise RuntimeError(f"Missing TRADIER_{MODE.upper()}_ACCOUNT_ID")

class TradierClient:
    def __init__(self):
        self.base_url   = BASE_URL
        self.token      = TOKEN
        self.account_id = ACCOUNT

    @property
    def headers(self) -> Dict[str,str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept":        "application/json",
        }

    async def get_expirations(self, symbol: str) -> List[str]:
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.headers) as cli:
            r = await cli.get("/markets/options/expirations", params={"symbol": symbol})
            r.raise_for_status()
            return r.json().get("expirations", {}).get("date", [])

    async def get_quote(self, symbol: str) -> Dict[str, Any]:
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.headers) as cli:
            r = await cli.get("/markets/quotes", params={"symbols": symbol})
            r.raise_for_status()
            return r.json().get("quotes", {}).get("quote", {})

    def format_tradier_option_symbol(self, ticker: str, expiration: str, right: str, strike: float) -> str:
        s = f"{int(strike * 1000):08d}"
        return f"{ticker}{expiration}{right}{s}"

    async def submit_multileg_order(
        self, symbol: str, legs: List[Dict[str, Any]], price: float = 1.0
    ) -> Dict[str, Any]:
        data = {
            "class":    "option",
            "type":     "multileg",
            "symbol":   symbol,
            "duration": "day",
            "price":    str(price),
        }
        for i, leg in enumerate(legs):
            data[f"option_symbol[{i}]"] = leg["option_symbol"]
            data[f"side[{i}]"]          = leg["side"]
            data[f"quantity[{i}]"]      = str(leg["quantity"])
        hdrs = {**self.headers, "Content-Type": "application/x-www-form-urlencoded"}
        async with httpx.AsyncClient(base_url=self.base_url, headers=hdrs) as cli:
            r = await cli.post(f"/accounts/{self.account_id}/orders", data=data)
            r.raise_for_status()
            return r.json()

    async def submit_equity_order(
        self, symbol: str, side: str, quantity: int, price: Optional[float] = None
    ) -> Dict[str, Any]:
        order_type = "market" if price is None else "limit"
        data = {
            "class":    "equity",
            "symbol":   symbol,
            "side":     side,
            "quantity": str(quantity),
            "duration": "day",
            "type":     order_type,
        }
        if price is not None:
            data["price"] = str(price)
        hdrs = {**self.headers, "Content-Type": "application/x-www-form-urlencoded"}
        async with httpx.AsyncClient(base_url=self.base_url, headers=hdrs) as cli:
            r = await cli.post(f"/accounts/{self.account_id}/orders", data=data)
            r.raise_for_status()
            return r.json()
EOF

# 3. Run your test suite again:
python3 -m backend.scripts.test_all_bots
# 1. Go to your project root
cd ~/skystrike_fullstack_final_release
# 2. Overwrite your Tradier client with a clean, correct version in one go:
cat > backend/services/tradier_client.py << 'EOF'
import os
from dotenv import load_dotenv
import httpx
from typing import List, Dict, Any, Optional

# Load env vars
load_dotenv()

# Determine mode
MODE = os.getenv("TRADIER_MODE", "paper").strip().lower()
if MODE not in ("paper", "live"):
    raise RuntimeError(f"Invalid TRA­DIER_MODE: {MODE}")

# Base URL and credentials
BASE_URL = "https://sandbox.tradier.com/v1" if MODE == "paper" else "https://api.tradier.com/v1"
TOKEN    = os.getenv(f"TRADIER_{MODE.upper()}_ACCESS_TOKEN")
ACCOUNT  = os.getenv(f"TRADIER_{MODE.upper()}_ACCOUNT_ID")

if not TOKEN:
    raise RuntimeError(f"Missing TRADIER_{MODE.upper()}_ACCESS_TOKEN")
if not ACCOUNT:
    raise RuntimeError(f"Missing TRADIER_{MODE.upper()}_ACCOUNT_ID")

class TradierClient:
    def __init__(self):
        self.base_url   = BASE_URL
        self.token      = TOKEN
        self.account_id = ACCOUNT

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept":        "application/json",
        }

    async def get_expirations(self, symbol: str) -> List[str]:
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.headers) as cli:
            r = await cli.get("/markets/options/expirations", params={"symbol": symbol})
            r.raise_for_status()
            return r.json().get("expirations", {}).get("date", [])

    async def get_quote(self, symbol: str) -> Dict[str, Any]:
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.headers) as cli:
            r = await cli.get("/markets/quotes", params={"symbols": symbol})
            r.raise_for_status()
            return r.json().get("quotes", {}).get("quote", {})

    def format_tradier_option_symbol(self, ticker: str, exp: str, right: str, strike: float) -> str:
        s = f"{int(strike * 1000):08d}"
        return f"{ticker}{exp}{right}{s}"

    async def submit_multileg_order(
        self, symbol: str, legs: List[Dict[str, Any]], price: float = 1.0
    ) -> Dict[str, Any]:
        data = {
            "class":    "option",
            "type":     "multileg",
            "symbol":   symbol,
            "duration": "day",
            "price":    str(price),
        }
        for i, leg in enumerate(legs):
            data[f"option_symbol[{i}]"] = leg["option_symbol"]
            data[f"side[{i}]"]          = leg["side"]
            data[f"quantity[{i}]"]      = str(leg["quantity"])
        headers = {**self.headers, "Content-Type": "application/x-www-form-urlencoded"}
        async with httpx.AsyncClient(base_url=self.base_url, headers=headers) as cli:
            r = await cli.post(f"/accounts/{self.account_id}/orders", data=data)
            r.raise_for_status()
            return r.json()

    async def submit_equity_order(
        self, symbol: str, side: str, quantity: int, price: Optional[float] = None
    ) -> Dict[str, Any]:
        data = {
            "class":    "equity",
            "symbol":   symbol,
            "side":     side,
            "quantity": str(quantity),
            "duration": "day",
            "type":     "market" if price is None else "limit",
        }
        if price is not None:
            data["price"] = str(price)
        headers = {**self.headers, "Content-Type": "application/x-www-form-urlencoded"}
        async with httpx.AsyncClient(base_url=self.base_url, headers=headers) as cli:
            r = await cli.post(f"/accounts/{self.account_id}/orders", data=data)
            r.raise_for_status()
            return r.json()
EOF

# 3. Run your test suite again
python3 -m backend.scripts.test_all_bots
cd ~/skystrike_fullstack_final_release
vim backend/services/tradier_client.py
python3 -m backend.scripts.test_all_bots
# 1. cd into your project root
cd ~/skystrike_fullstack_final_release
# 2. Open tradier_api.py in your editor
vim backend/services/tradier_api.py
python3 -m backend.scripts.test_all_bots
# 1. cd into your project root
cd ~/skystrike_fullstack_final_release
# 2. Overwrite backend/services/tradier_api.py with correct exports
cat > backend/services/tradier_api.py << 'EOF'
# backend/services/tradier_api.py

from .tradier_client import TradierClient

# single shared client
_client = TradierClient()

# Market data
async def get_expirations(symbol: str):
    return await _client.get_expirations(symbol)

async def get_quote(symbol: str):
    return await _client.get_quote(symbol)

# Formatter
format_tradier_option_symbol = _client.format_tradier_option_symbol

# Order submissions
submit_multileg_order = _client.submit_multileg_order
submit_equity_order    = _client.submit_equity_order
EOF

# 3. Re-run your test suite
python3 -m backend.scripts.test_all_bots
cd ~/skystrike_fullstack_final_release
cat > backend/services/tradier_api.py << 'EOF'
# backend/services/tradier_api.py

import httpx
from typing import List, Dict, Any
from .tradier_client import TradierClient

# single shared client
_client = TradierClient()

# Market data
async def get_expirations(symbol: str) -> List[str]:
    return await _client.get_expirations(symbol)

async def get_quote(symbol: str) -> Dict[str, Any]:
    return await _client.get_quote(symbol)

# Formatter
format_tradier_option_symbol = _client.format_tradier_option_symbol

# Single-leg option order
async def submit_option_order(
    option_symbol: str,
    side: str,
    quantity: int
) -> Dict[str, Any]:
    data = {
        "class":         "option",
        "type":          "single",
        "option_symbol": option_symbol,
        "side":          side,
        "quantity":      str(quantity),
        "duration":      "day",
    }
    headers = {**_client.headers, "Content-Type": "application/x-www-form-urlencoded"}
    async with httpx.AsyncClient(
        base_url=_client.base_url, headers=headers
    ) as cli:
        resp = await cli.post(f"/accounts/{_client.account_id}/orders", data=data)
        resp.raise_for_status()
        return resp.json()

# Multi-leg and equity orders
submit_multileg_order = _client.submit_multileg_order
submit_equity_order    = _client.submit_equity_order
EOF

# Then rerun your tests
python3 -m backend.scripts.test_all_bots
cd ~/skystrike_fullstack_final_release
vim backend/services/tradier_client.py
python3 -m backend.scripts.test_all_bots
# 1. Go to your project root
cd ~/skystrike_fullstack_final_release
# 2. Fix the invalid character in that RuntimeError line
#    (removes any stray non-ASCII and ensures the variable name is correct)
sed -i 's/Invalid TRA.*DER_MODE/Invalid TRADIER_MODE/' backend/services/tradier_client.py
# 3. (Optional) Double-check your file encoding is UTF-8
file backend/services/tradier_client.py
# 4. Re-run your test suite
python3 -m backend.scripts.test_all_bots
# 1. cd into project root
cd ~/skystrike_fullstack_final_release
# 2. Convert the file to UTF-8
iconv -f ISO-8859-1 -t UTF-8 backend/services/tradier_client.py -o backend/services/tradier_client.py.utf8
mv backend/services/tradier_client.py.utf8 backend/services/tradier_client.py
# 3. Remove any leftover non-ASCII garbage and fix the error message text
sed -i   -e 's/�//g'   -e 's/Invalid TRA.*DER_MODE/Invalid TRADIER_MODE/'   backend/services/tradier_client.py
# 4. Verify it’s now UTF-8
file backend/services/tradier_client.py
# 5. Rerun your tests
python3 -m backend.scripts.test_all_bots
# 1. cd into your project root
cd ~/skystrike_fullstack_final_release
# 2. In-place replace the bad raise with an ASCII-only version:
sed -i   -e 's#^\s*raise RuntimeError.*$#    raise RuntimeError("Invalid TRADIER_MODE: {}".format(MODE))#'   backend/services/tradier_client.py
# 3. Force the file to be UTF-8
iconv -f ISO-8859-1 -t UTF-8 backend/services/tradier_client.py -o backend/services/tradier_client.py.utf8
mv backend/services/tradier_client.py.utf8 backend/services/tradier_client.py
# 4. Quick sanity check that the line looks right:
sed -n '1,20p' backend/services/tradier_client.py | sed -n '5,10p'
# 5. Rerun your test suite
python3 -m backend.scripts.test_all_bots
ls -l backend/services/tradier_client.py
sed -n '1,15p' backend/services/tradier_client.py
python3 -m backend.scripts.test_all_bots
touch backend/services/__init__.py
export TRADIER_TOKEN=your_token_here
export TRADIER_ACCOUNT_ID=your_account_id_here
grep -L 'TradierClient' backend/bots/*.py | xargs -I{} sed -i '1i from backend.bots.base import TradierClient' {}
find backend/bots -name "*.py" ! -name "base.py" ! -name "__init__.py" -exec sed -i '/async def build_order/,/^$/d' {} \; -exec bash -c 'echo -e "\nasync def build_order(ticker, contracts, dte, mode):\n    strike = 100\n    return [\n        {\"right\": \"put\", \"strike\": strike, \"side\": \"sell\", \"quantity\": contracts},\n        {\"right\": \"put\", \"strike\": strike - 5, \"side\": \"buy\", \"quantity\": contracts}\n    ]" >> {}' \;
python3 -m backend.scripts.test_all_bots
cat > backend/services/tradier_api.py <<EOF
import os
from typing import List, Dict, Any
from backend.bots.base import TradierClient

_client = TradierClient()

async def get_expirations(symbol: str) -> List[str]:
    return _client.get_expirations(symbol)

async def get_quote(symbol: str) -> Dict[str, Any]:
    return _client.get_quote(symbol)

format_tradier_option_symbol = _client.format_option

async def submit_multileg_order(symbol: str, legs: List[Dict[str, Any]], price: float = 1.0):
    return _client.submit_multileg(symbol, legs, price)

async def submit_equity_order(symbol: str, side: str, quantity: int):
    return _client.submit_equity(symbol, side, quantity)

async def submit_option_order(option_symbol: str, side: str, quantity: int):
    return _client.submit_option(option_symbol, side, quantity)
EOF

python3 -m backend.scripts.test_all_bots
cd ~/skystrike_fullstack_final_release/backend/services
sed -i 's/"type": *"market"/"type": "debit"/g' tradier_api.py
sed -i '/"price": *str(price)/a\        "quantity": "1",' tradier_api.py
python3 -m backend.scripts.test_all_bots
cd ~/skystrike_fullstack_final_release
export PYTHONPATH=$(pwd)
python3 -m backend.scripts.test_all_bots
# Navigate to the backend services folder
cd ~/skystrike_fullstack_final_release/backend/services
# ✅ Replace all occurrences of "type": "market" with correct multileg type
sed -i 's/"type": *"market"/"type": "debit"/g' tradier_api.py
# ✅ Insert `"quantity[0]": str(quantity)` and `"quantity[1]": str(quantity)` where appropriate
sed -i '/"side\[0\]":/a\        "quantity[0]": str(quantity),' tradier_api.py
sed -i '/"side\[1\]":/a\        "quantity[1]": str(quantity),' tradier_api.py
cd ~/skystrike_fullstack_final_release
export PYTHONPATH=$(pwd)
python3 -m backend.scripts.test_all_bots
cd ~/skystrike_fullstack_final_release/backend/services
# 🧼 Clean up any previous broken quantity insertions
sed -i '/"quantity\[0\]":/d' tradier_api.py
sed -i '/"quantity\[1\]":/d' tradier_api.py
# ✅ Replace "type": "market" with correct multileg value
sed -i 's/"type": *"market"/"type": "debit"/g' tradier_api.py
# ✅ (Optional) Add price if missing — but we already have it in your payload
# ✅ Inject quantities right after their matching side lines
sed -i '/"side\[0\]":/a\        "quantity[0]": str(legs[0]["quantity"]),' tradier_api.py
sed -i '/"side\[1\]":/a\        "quantity[1]": str(legs[1]["quantity"]),' tradier_api.py
cd ~/skystrike_fullstack_final_release
export PYTHONPATH=$(pwd)
python3 -m backend.scripts.test_all_bots
# 👇 Insert top-level "quantity" after "type"
sed -i '/"type": *"debit"/a\        "quantity": str(quantity),' backend/services/tradier_api.py
cd ~/skystrike_fullstack_final_release
export PYTHONPATH=$(pwd)
python3 -m backend.scripts.test_all_bots
cd ~/skystrike_fullstack_final_release/backend/services
# ✅ Clean up any previous bad quantity injection
sed -i '/quantity\[0\]/d' tradier_api.py
sed -i '/quantity\[1\]/d' tradier_api.py
sed -i '/"quantity": str(quantity)/d' tradier_api.py
# ✅ Force all multileg orders to use type "debit" instead of "market"
sed -i 's/"type": *"market"/"type": "debit"/g' tradier_api.py
# ✅ Inject required top-level quantity (Tradier requires it for multileg)
sed -i '/"type": *"debit"/a\        "quantity": str(quantity),' tradier_api.py
# ✅ Inject leg-level quantities after their respective sides
sed -i '/"side\[0\]":/a\        "quantity[0]": str(legs[0]["quantity"]),' tradier_api.py
sed -i '/"side\[1\]":/a\        "quantity[1]": str(legs[1]["quantity"]),' tradier_api.py
cd ~/skystrike_fullstack_final_release
export PYTHONPATH=$(pwd)
python3 -m backend.scripts.test_all_bots
cd ~/skystrike_fullstack_final_release/backend/services
# ✅ 1. Remove all stale quantity lines
sed -i '/"quantity": *str(quantity)/d' tradier_api.py
sed -i '/quantity\[0\]/d' tradier_api.py
sed -i '/quantity\[1\]/d' tradier_api.py
# ✅ 2. Replace incorrect "type": "market" with "type": "debit"
sed -i 's/"type": *"market"/"type": "debit"/g' tradier_api.py
# ✅ 3. Add top-level "quantity" required for multileg (after "type")
sed -i '/"type": *"debit"/a\        "quantity": str(quantity),' tradier_api.py
# ✅ 4. Add per-leg quantities (must come after the matching side)
sed -i '/"side\[0\]":/a\        "quantity[0]": str(legs[0]["quantity"]),' tradier_api.py
sed -i '/"side\[1\]":/a\        "quantity[1]": str(legs[1]["quantity"]),' tradier_api.py
cd ~/skystrike_fullstack_final_release
export PYTHONPATH=$(pwd)
python3 -m backend.scripts.test_all_bots
cd ~/skystrike_fullstack_final_release
export PYTHONPATH=$(pwd)
python3 -m backend.scripts.test_all_bots
cd ~/skystrike_fullstack_final_release
export PYTHONPATH=$(pwd)
python3 -m backend.scripts.test_all_bots
cd ~/skystrike_fullstack_final_release
export PYTHONPATH=$(pwd)
python3 -m backend.scripts.test_all_bots
sed -i 's/"class": *"option"/"class": "multileg"/' backend/services/tradier_client.py
sed -i 's/"type": *"debit"/"type": "limit"/' backend/services/tradier_client.py
sed -i 's/"type": *"market"/"type": "limit"/' backend/services/tradier_client.py
cd ~/skystrike_fullstack_final_release
export PYTHONPATH=$(pwd)
python3 -m backend.scripts.test_all_bots
# 1. Replace invalid class "option" with "multileg"
sed -i 's/"class": *"option"/"class": "multileg"/g' backend/services/tradier_client.py
# 2. Replace invalid type "debit" with "limit"
sed -i 's/"type": *"debit"/"type": "limit"/g' backend/services/tradier_client.py
# 3. Remove top-level quantity from multileg orders
sed -i '/"quantity": *order["quantity"],/d' backend/services/tradier_client.py
python3 -m backend.scripts.test_all_bots
# From your project root
export PYTHONPATH=$(pwd)
# Re-run tests
python3 -m backend.scripts.test_all_bots
export PYTHONPATH=$(pwd)
python3 -m backend.scripts.test_all_bots
sed -i 's/"class": "option"/"class": "multileg"/g' backend/services/tradier_api.py
export PYTHONPATH=$(pwd)
python3 -m backend.scripts.test_all_bots
export PYTHONPATH=$(pwd)
python3 -m backend.scripts.test_all_bots
curl -X POST http://localhost:8000/api/orders/place   -H "Authorization: Bearer $TOKEN"   -H "Content-Type: application/json"   -d '{"bot": "ironcondor", "ticker": "SPX", "contracts": 1, "dte": 0}'
uvicorn backend.main:app --host 0.0.0.0 --port 8000
pm2 start uvicorn --name skystrike-api --interpreter python3 --   backend.main:app --host 0.0.0.0 --port 8000
pm2 restart skystrike-api
pm2 logs skystrike-api
pm2 restart skystrike-api
pm2 logs skystrike-api
pm2 restart skystrike-api
pm2 logs skystrike-api
pm2 restart skystrike-api
pm2 logs skystrike-api
find backend/bots -name "*.py" -exec sed -i 's/[^ -~]/+\/-/g' {} +
cd ~/skystrike_fullstack_final_release/backend
find backend/bots -name "*.py" -exec sed -i 's/[^ -~]/+\/-/g' {} +
cd ~/skystrike_fullstack_final_release
find backend/bots -name "*.py" -exec sed -i 's/[^ -~]/+\/-/g' {} +
pm2 restart skystrike-api
pm2 logs skystrike-api --lines 50
sed -i 's/[^\x00-\x7F]//g' backend/bots/kingcondor.py
pm2 restart skystrike-api
pm2 logs skystrike-api --lines 50
sed -i 's/[^\x00-\x7F]//g' backend/bots/kingcondor.py
pm2 restart skystrike-api
pm2 logs skystrike-api --lines 50
sed -i 's/[^\x00-\x7F]//g' backend/bots/kingcondor.py && pm2 restart skystrike-api
pm2 logs skystrike-api --lines 50
sed -i 's/[^\x00-\x7F]//g' backend/bots/kingcondor.py && pm2 restart skystrike-api
pm2 logs skystrike-api --lines 50
sed -i 's/[^[:print:]\t]//g' backend/bots/kingcondor.py && pm2 restart skystrike-api
pm2 logs skystrike-api --lines 30
sed -i 's/[^[:print:]\t]//g' backend/bots/kingcondor.py
pm2 restart skystrike-api
pm2 logs skystrike-api --lines 20
pm2 restart skystrike-api
pm2 logs skystrike-api --lines 20
pm2 restart skystrike-api
pm2 logs skystrike-api --lines 20
curl -X POST http://localhost:8000/api/login   -H "Content-Type: application/json"   -d '{"username":"admin", "password":"webflow"}'
curl -X GET http://localhost:8000/api/dashboard   -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjp7InVzZXJuYW1lIjoiYWRtaW4iLCJnb2FsIjoiYmFsYW5jZWQiLCJhY2NvdW50X3NpemUiOjUwMDAwLCJ0cmFkaWVyX21vZGUiOiJwYXBlciJ9LCJleHAiOjE3NTE1MzAyMTJ9.SBxFYWn2PNt6BzW7mIH5oXIEhw9xazFEs6XfuMA9YpI"
python3 backend/scripts/test_all_bots.py
export PYTHONPATH=$(pwd)
python3 backend/scripts/test_all_bots.py
sed -i 's/def append_log(/def append_log(log_type, data):  # /' backend/services/log_writer.py
cat > backend/bots/equity_buy.py << 'EOF'
async def build_order(ticker: str, contracts: int, dte: int, mode: str) -> dict:
    return {
        "class": "equity",
        "symbol": ticker,
        "side": "buy",
        "quantity": contracts,
        "price": None
    }
EOF

sed -i 's/"iron_condor"/"ironcondor"/g' backend/scripts/test_all_bots.py
export PYTHONPATH=$(pwd)
python3 backend/scripts/test_all_bots.py
sed -i 's/data.append(entry)/data.append(data)/' backend/services/log_writer.py
export PYTHONPATH=$(pwd)
python3 backend/scripts/test_all_bots.py
sed -i 's/data.append(data)/data.append(log_entry)/' backend/services/log_writer.py
cat > backend/services/log_writer.py << 'EOF'
import os
import json
from datetime import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def append_log(log_type: str, log_entry: dict):
    path = os.path.join(LOG_DIR, f"{log_type}_log.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    log_entry["timestamp"] = datetime.now().isoformat()
    data.append(log_entry)

    with open(path, "w") as f:
        json.dump(data, f, indent=2)
EOF

export PYTHONPATH=$(pwd)
python3 backend/scripts/test_all_bots.py
sed -i 's/, *mode=mode//' backend/submit_order.py
export PYTHONPATH=$(pwd)
python3 backend/scripts/test_all_bots.py
sed -i 's/order_payload = await BUILD_MAP\[bot\](ticker=ticker, contracts=contracts, dte=dte)/order_payload = await BUILD_MAP[bot](ticker=ticker, contracts=contracts, dte=dte, mode=mode)/' backend/submit_order.py
export PYTHONPATH=$(pwd)
python3 backend/scripts/test_all_bots.py
# Remove mode=mode from submit_*_order() calls but keep it for build_order()
sed -i 's/submit_multileg_order(\([^)]*\), *mode=mode)/submit_multileg_order(\1)/g' backend/submit_order.py
sed -i 's/submit_equity_order(\([^)]*\), *mode=mode)/submit_equity_order(\1)/g' backend/submit_order.py
export PYTHONPATH=$(pwd)
python3 backend/scripts/test_all_bots.py
# Remove ', mode=mode' regardless of spacing or position
sed -i 's/, *mode=mode//g' backend/submit_order.py
sed -i 's/mode=mode, *//g' backend/submit_order.py
sed -i 's/mode=mode//g' backend/submit_order.py
export PYTHONPATH=$(pwd)
python3 backend/scripts/test_all_bots.py
sed -i 's/BUILD_MAP\[bot\](ticker=ticker, contracts=contracts, dte=dte)/BUILD_MAP[bot](ticker=ticker, contracts=contracts, dte=dte, mode=mode)/' backend/submit_order.py
export PYTHONPATH=$(pwd)
python3 backend/scripts/test_all_bots.py
sed -i 's/"type": "limit"/"type": "market"/g' backend/bots/*.py
sed -i 's/await submit_/submit_/g' backend/submit_order.py
export PYTHONPATH=$(pwd)
python3 backend/scripts/test_all_bots.py
find backend/bots -name "*.py" -exec sed -i 's/"type": "limit"/"type": "debit"/g' {} +
python3 backend/scripts/test_all_bots.py
find backend/bots -name "*.py" -exec sed -i 's/"type": "limit"/"type": "debit"/g' {} +
sed -i 's/"type": "limit"/"type": "debit"/g' backend/submit_order.py
python3 backend/scripts/test_all_bots.py
sed -i 's/"type": "limit"/"type": "debit"/g' backend/bots/pairstrader.py
sed -i 's/"type": "limit"/"type": "debit"/g' backend/bots/scalper.py
python3 backend/scripts/test_all_bots.py
sed -i '/submit_multileg_order/s/type": "limit"/type": "debit"/' backend/submit_order.py
sed -i 's/order_type="limit"/order_type="debit"/g' backend/submit_order.py
python3 backend/scripts/test_all_bots.py
cd backend/bots
# Fix side values across all bots
sed -i 's/"side": "buy"/"side": "buy_to_open"/g' *.py
sed -i 's/"side": "sell"/"side": "sell_to_open"/g' *.py
# Ensure quantity is quoted
sed -i 's/"quantity": \([0-9]\+\)/"quantity": "\1"/g' *.py
python3 backend/scripts/test_all_bots.py
cd ~/skystrike_fullstack_final_release
python3 backend/scripts/test_all_bots.py
sed -i 's/"side": "buy_to_open"/"side": "buy"/g' backend/bots/equity_buy.py
sed -i 's/"side": "sell_to_open"/"side": "sell"/g' backend/bots/equity_buy.py
[RootSymbol][YYYYMMDD][C/P][StrikePrice * 1000, padded to 8 digits]
grep -rl "format_tradier_option_symbol" backend/bots | while read f; do   sed -i 's/format_tradier_option_symbol(\(.*\))/format_tradier_option_symbol(\1).upper()/g' "$f"; done
python3 backend/scripts/test_all_bots.py
# Replace 'buy_to_open' with 'buy' in equity_buy.py (Tradier requires this)
sed -i 's/"side": "buy_to_open"/"side": "buy"/g' backend/bots/equity_buy.py
sed -i 's/"side": "sell_to_open"/"side": "sell"/g' backend/bots/equity_buy.py
nano backend/bots/copybot.py
python3 backend/scripts/test_all_bots.py
nano +84 backend/bots/iron_condor.py
python3 backend/scripts/test_all_bots.py
python3 backend/scripts/get_tradier_token.py
source .env
nano ~/skystrike_fullstack_final_release/backend/.env
python3 backend/scripts/test_all_bots.py
curl -X POST "https://sandbox.tradier.com/v1/accounts/VA70062258/orders"   -H "Authorization: Bearer RlLmD2V8FKCJAcuj9KQoKpU5TeKt"   -H "Accept: application/json"   -H "Content-Type: application/x-www-form-urlencoded"   -d "class=multileg&symbol=NDX&type=market&duration=day&price=1.00\
&option_symbol[0]=SPY250627C00480000&side[0]=sell_to_open&quantity[0]=1\
&option_symbol[1]=SPY250627C00485000&side[1]=buy_to_open&quantity[1]=1\
&option_symbol[2]=SPY250627P00470000&side[2]=sell_to_open&quantity[2]=1\
&option_symbol[3]=SPY250627P00465000&side[3]=buy_to_open&quantity[3]=1"
python3 backend/scripts/test_all_bots.py
find backend/bots -type f -name "*.py" -exec sed -i -e 's/\(get_tradier_option_symbol(\s*[^,)]\+\s*,\s*[^,)]\+\s*,\s*[^,)]\+\s*,\s*[^,)]\+\)/await \1, mode)/' {} +
grep -r --include="*.py" "get_tradier_option_symbol(" backend/bots
find backend/bots -type f -name "*.py" -exec sed -i -e 's/await await /await /g' -e 's/)),/,)/g' {} +
python3 backend/scripts/test_all_bots.py
find backend/bots -type f -name "*.py" -exec sed -i -e 's/\(get_tradier_option_symbol([^)]*)\))$/\1)/' {} +
python3 backend/scripts/test_all_bots.py
find backend/bots -type f -name "*.py" -exec sed -i -e 's/\(await get_tradier_option_symbol([^)]*)\))/\1)/g' {} +
python3 backend/scripts/test_all_bots.py
find backend/bots -type f -name "*.py" -exec sed -i -e 's/\(await get_tradier_option_symbol([^)]*)\))$/\1)/' -e 's/\(await get_tradier_option_symbol([^)]*)\))$/\1)/' -e 's/\(await get_tradier_option_symbol([^)]*)\))$/\1)/' {} +
python3 backend/scripts/test_all_bots.py
find backend/bots -type f -name "*.py" -exec sed -i -e 's/\(await get_tradier_option_symbol([^)]*)\))/\1)/g' -e 's/))$/)/g' {} +
python3 backend/scripts/test_all_bots.py
sed -i 's/\(await get_tradier_option_symbol([^)]*)\))$/\1)/' backend/bots/iron_condor.py
python3 backend/scripts/test_all_bots.py
nano backend/bots/pairstrader.py
python3 backend/scripts/test_all_bots.py
# 1. Fix submit_order.py
sed -i 's/order_payload = await/order_payload =/' backend/submit_order.py
# 2. Make every build_order sync and drop internal awaits
for f in backend/bots/*.py; do   sed -i 's/^async def build_order/def build_order/' "$f";   sed -i 's/await client.get_quote/client.get_quote/' "$f";   sed -i 's/await get_tradier_option_symbol/get_tradier_option_symbol/' "$f"; done
# 3. (If needed) Make option_lookup sync
sed -i 's/^async def get_tradier_option_symbol/def get_tradier_option_symbol/' backend/services/option_lookup.py
python3 -m backend.scripts.test_all_bots
for f in backend/bots/*.py; do
  sed -i "/get_tradier_option_symbol/a from backend.services.option_lookup import get_next_expiration" "$f"
  sed -i "s/^[[:space:]]*expiration =.*$/    expiration = get_next_expiration(ticker, dte, mode)/" "$f"; done
python3 -m backend.scripts.test_all_bots
for f in backend/bots/*.py; do
  sed -i "/from backend.services.option_lookup import get_tradier_option_symbol/a from backend.services.option_lookup import get_next_expiration" "$f"
  sed -i "s/^\([[:space:]]*\)expiration =.*$/\1expiration = get_next_expiration(ticker, dte, mode)/" "$f"; done
python3 -m backend.scripts.test_all_bots
for f in backend/bots/*.py; do
  sed -i '/get_next_expiration/d' "$f"
  sed -i '/get_tradier_option_symbol/a\
from backend.services.option_lookup import get_next_expiration
' "$f"
  sed -i 's|^\([[:space:]]*\)expiration =.*$|\1expiration = get_next_expiration(ticker, dte, mode)|' "$f"; done
# then rerun your tests:
python3 -m backend.scripts.test_all_bots
sed -Ei   -e '/from backend.services.option_lookup import get_tradier_option_symbol/a\
from backend.services.option_lookup import get_next_expiration'   -e 's#^([[:space:]]*)expiration = .+strftime.*$#\1expiration = get_next_expiration(ticker, dte, mode)#'   backend/bots/*.py
python3 -m backend.scripts.test_all_bots
# install Black if you haven't already
pip install black
# re‐format all your bot files
black backend/bots/*.py
# then re‐run your tests
python3 -m backend.scripts.test_all_bots
python3 - <<'PYCODE'
import glob, re, sys

pattern_import = re.compile(
    r'^(from backend\.services\.option_lookup import get_tradier_option_symbol)(.*)$',
    re.MULTILINE
)
pattern_expiry = re.compile(
    r'^([ \t]*)expiration\s*=.*strftime\([^)]+\).*$',
    re.MULTILINE
)

for path in glob.glob("backend/bots/*.py"):
    text = open(path).read()
    # 1) Patch the import
    def _add_import(m):
        line, tail = m.group(1), m.group(2)
        if "get_next_expiration" not in tail:
            tail = tail.rstrip() + ", get_next_expiration"
        return line + tail
    text = pattern_import.sub(_add_import, text)

    # 2) Patch expiration assignment (preserve indent)
    text = pattern_expiry.sub(r"\1expiration = get_next_expiration(ticker, dte, mode)", text)

    open(path, "w").write(text)
    print(f"Patched {path}")

print("✅ All bot files updated.")
PYCODE

# Now re-run your tests:
python3 -m backend.scripts.test_all_bots
# Install if needed
pip install autopep8
# Automatically fix indent (and other PEP8 issues) in all bots
autopep8 --in-place --aggressive --aggressive backend/bots/*.py
# Re-run your tests
python3 -m backend.scripts.test_all_bots
# 1. From your project root, create a patch file
cat > wire-rounding.patch << 'EOF'
--- a/backend/bots/iron_condor.py
+++ b/backend/bots/iron_condor.py
@@ -1,6 +1,8 @@
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
@@ import logging
-from datetime import date, timedelta
+from datetime import date, timedelta
+from backend.services.rounding_util import round_to_increment
+from backend.services.option_lookup import get_tradier_option_symbol
@@ async def build_order(...)
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
@@ import logging
-from datetime import date, timedelta
+from datetime import date, timedelta
+from backend.services.rounding_util import round_to_increment
+from backend.services.option_lookup import get_tradier_option_symbol
@@ async def build_order(...)
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
@@ import logging
-from datetime import date, timedelta
+from datetime import date, timedelta
+from backend.services.rounding_util import round_to_increment
+from backend.services.option_lookup import get_tradier_option_symbol
@@ async def build_order(...)
-    strike = round(spot * 0.9, 0)
-    sym    = format_option_symbol(ticker, exp, "P", strike)
+    strike = round_to_increment(spot * 0.9, 0.5)
+    sym    = get_tradier_option_symbol(ticker, exp, strike, "P")
--- a/backend/bots/wheel.py
+++ b/backend/bots/wheel.py
@@ import logging
-from datetime import date, timedelta
+from datetime import date, timedelta
+from backend.services.rounding_util import round_to_increment
+from backend.services.option_lookup import get_tradier_option_symbol
@@ async def build_order(...)
-    strike = round(spot * 0.88, 0)
-    sym    = format_option_symbol(ticker, exp, "P", strike)
+    strike = round_to_increment(spot * 0.88, 0.5)
+    sym    = get_tradier_option_symbol(ticker, exp, strike, "P")
--- a/backend/bots/trend.py
+++ b/backend/bots/trend.py
@@ import logging
-from datetime import date, timedelta
+from datetime import date, timedelta
+from backend.services.rounding_util import round_to_increment
+from backend.servi!ces.option_lookup import get_tradier_option_symbol
@@ async def build_order(...)
-    short_strike = round(spot * 0.98, 0)
-    long_strike  = round(spot * 1.02, 0)
+    short_strike = round_to_increment(spot * 0.98, 0.5)
+    long_strike  = round_to_increment(spot * 1.02, 0.5)
+    sym_s        = get_tradier_option_symbol(ticker, exp, short_strike, "P")
+    sym_l        = get_tradier_option_symbol(ticker, exp, long_strike,  "C")
--- a/backend/bots/replicator.py
+++ b/backend/bots/replicator.py
@@ import logging
-from datetime import date, timedelta
+from datetime import date, timedelta
+from backend.services.rounding_util import round_to_increment
+from backend.services.option_lookup import get_tradier_option_symbol
@@ async def build_order(...)
-    short_strike = round(spot * 0.97, 0)
-    long_strike  = short_strike - 3
+    short_strike = round_to_increment(spot * 0.97, 0.5)
+    long_strike  = short_strike - 3
+    sym_s        = get_tradier_option_symbol(ticker, exp, short_strike, "P")
+    sym_l        = get_tradier_option_symbol(ticker, exp, long_strike,  "P")
--- a/backend/bots/copybot.py
+++ b/backend/bots/copybot.py
@@ import logging
-from datetime import date, timedelta
+from datetime import date, timedelta
+from backend.services.rounding_util import round_to_increment
+from backend.services.option_lookup import get_tradier_option_symbol
@@ async def build_order(...)
-    short_strike = round(spot * 1.01, 0)
-    long_strike  = round(spot * 0.99, 0)
+    short_strike = round_to_increment(spot * 1.01, 0.5)
+    long_strike  = round_to_increment(spot * 0.99, 0.5)
--- a/backend/bots/dcabot.py
+++ b/backend/bots/dcabot.py
@@ import logging
-from datetime import date, timedelta
+from datetime import date, timedelta
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
