from dotenv import load_dotenv
load_dotenv()

import logging
import pkgutil
import importlib

from backend.bots import BUILD_MAP
from backend.services.tradier_client import TradierClient
from backend.services.log_writer import append_log

logger = logging.getLogger("skystrike.submit")

async def run_bot_with_params(
    bot: str,
    ticker: str,
    contracts: int = 1,
    dte: int = 1,
    mode: str = "paper"
):
    if bot not in BUILD_MAP:
        return {"error": f"Bot '{bot}' not supported."}

    try:
        logger.info(f"Building {bot} order: {ticker}, contracts={contracts}, dte={dte}, mode={mode}")
        build_fn = BUILD_MAP[bot]
        order_payload = await build_fn(ticker=ticker, contracts=contracts, dte=dte, mode=mode)

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

        def normalize_option_side(s: str) -> str:
            s = s.lower()
            if s in ("buy", "buy_to_open", "bto"):
                return "buy_to_open"
            if s in ("sell", "sell_to_open", "sto"):
                return "sell_to_open"
            return s

        client = TradierClient(mode=mode)

        if "legs" in order_payload and isinstance(order_payload["legs"], list):
            for leg in order_payload["legs"]:
                leg["side"] = normalize_option_side(leg.get("side", ""))
            response = await client.submit_multileg(
                symbol=ticker,
                legs=order_payload["legs"],
                price=order_payload.get("price", 1.0)
            )

        elif "option_symbol" in order_payload:
            side = normalize_option_side(order_payload.get("side", ""))
            response = await client.submit_option_order(
                option_symbol=order_payload["option_symbol"],
                side=side,
                quantity=order_payload["quantity"],
                price=order_payload.get("price")
            )

        elif order_payload.get("class", "").lower() == "equity":
            raw_side = order_payload.get("side", "").lower()
            eq_side = "buy" if raw_side.startswith("buy") else "sell"
            response = await client.submit_equity(
                symbol=order_payload["symbol"],
                side=eq_side,
                qty=order_payload["quantity"],
                price=order_payload.get("price")
            )

        else:
            return {"error": f"Unsupported order structure returned by bot '{bot}'."}

        return {"status": "success", "response": response}

    except Exception as e:
        logger.exception(f"Error running bot '{bot}': {e}")
        return {"error": str(e)}
