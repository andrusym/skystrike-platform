import traceback
from datetime import datetime, timedelta, date
from backend.services.tradier_client import TradierClient
from backend.services.log_writer import append_log
from backend.shared.utils import get_expirations, format_tradier_option_symbol

# Instantiate a single TradierClient
_client = TradierClient()

def build_order(
    ticker: str,
    contracts: int,
    dte: int,
    confidence: float,
    mode: str
) -> dict:
    """
    Build an options order for the given parameters.
    """
    try:
        quote = _client.get_quote(ticker)
        mid = quote.get("last", 0)
        expirations = get_expirations(dte + 1)
        exp = expirations[dte]
        strike = round(mid)
        option_symbol = format_tradier_option_symbol(ticker, exp, "P", strike)
        return {
            "symbol": option_symbol,
            "quantity": contracts,
            "side": "buy_to_open",
            "type": "market",
            "tag": f"{ticker}_stub",
        }
    except Exception as e:
        raise RuntimeError(f"Failed to build order: {e}")

def run_bot_with_params(
    ticker: str,
    contracts: int,
    dte: int,
    mode: str
) -> dict:
    """
    Orchestrator entrypoint: builds and submits the order, then logs it.
    """
    try:
        order = build_order(ticker, contracts, dte, mode)
        # Submit via TradierClient; use sync or async as appropriate
        result = _client.place_order(order, mode=mode)
        append_log("trade_log.json", {
            "timestamp": datetime.now().isoformat(),
            "bot":       __name__,
            "ticker":    ticker,
            "order":     order,
            "result":    result,
        })
        return result
    except Exception as e:
        error_msg = f"{__name__}.run_bot_with_params error: {e}\n{traceback.format_exc()}"
        append_log("logs/errors.json", {"error": error_msg})
        return {"error": error_msg}
