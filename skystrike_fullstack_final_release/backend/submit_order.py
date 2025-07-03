import logging
import pkgutil
import importlib

from backend.bots import __path__ as bots_path
from backend.services.tradier_api import (
    submit_multileg_order,
    submit_option_order,
    submit_equity_order,
)
from backend.services.log_writer import append_log

logger = logging.getLogger("skystrike.submit")

# Automatically discover all bots in backend/bots/
BUILD_MAP = {}
for _, module_name, ispkg in pkgutil.iter_modules(bots_path):
    module = importlib.import_module(f"backend.bots.{module_name}")
    build_fn = getattr(module, "build_order", None)
    if callable(build_fn):
        BUILD_MAP[module_name] = build_fn


async def run_bot_with_params(
    bot: str,
    ticker: str,
    contracts: int = 1,
    dte: int = 1,
    mode: str = "paper"
):
    """
    Build and submit an order for the given bot.

    mode: "paper" for sandbox/paper trading, "live" for real account.
    """
    if bot not in BUILD_MAP:
        return {"error": f"Bot '{bot}' not supported."}

    try:
        logger.info(
            f"Building {bot} order: ticker={ticker}, "
            f"contracts={contracts}, dte={dte}, mode={mode}"
        )
        order_payload = await BUILD_MAP[bot](
            ticker=ticker,
            contracts=contracts,
            dte=dte,
            mode=mode
        )

        if not isinstance(order_payload, dict):
            return {"error": f"{bot} returned invalid payload type: {type(order_payload)}"}

        append_log("orders", {
            "bot": bot,
            "ticker": ticker,
            "contracts": contracts,
            "dte": dte,
            "mode": mode,
            "order": order_payload,
        })

        # normalize option sides
        def normalize_option_side(s: str) -> str:
            s = s.lower()
            if s in ("buy", "buy_to_open", "bto"):
                return "buy_to_open"
            if s in ("sell", "sell_to_open", "sto"):
                return "sell_to_open"
            return s

        # multi-leg order
        if "legs" in order_payload and isinstance(order_payload["legs"], list):
            for leg in order_payload["legs"]:
                leg["side"] = normalize_option_side(leg.get("side", ""))
            response = submit_multileg_order(
                symbol=ticker,
                legs=order_payload["legs"],
                price=order_payload.get("price", 1.0)
            )

        # single-leg option
        elif "option_symbol" in order_payload:
            side = normalize_option_side(order_payload.get("side", ""))
            response = submit_option_order(
                option_symbol=order_payload["option_symbol"],
                side=side,
                quantity=order_payload["quantity"],
                price=order_payload.get("price")
            )

        # equity order
        elif order_payload.get("class", "").lower() == "equity":
            raw_side = order_payload.get("side", "").lower()
            if raw_side.endswith("_to_open"):
                eq_side = "buy" if raw_side.startswith("buy") else "sell"
            else:
                eq_side = raw_side
            response = submit_equity_order(
                symbol=order_payload["symbol"],
                side=eq_side,
                quantity=order_payload["quantity"],
                price=order_payload.get("price")
            )

        else:
            return {"error": f"Unsupported order structure from bot '{bot}'."}

        return {"status": "success", "response": response}

    except Exception as e:
        logger.exception(f"Error running bot '{bot}': {e}")
        return {"error": str(e)}
