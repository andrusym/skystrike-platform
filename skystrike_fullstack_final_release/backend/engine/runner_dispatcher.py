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
