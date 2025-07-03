import logging

from backend.db.session                 import SessionLocal
from backend.db.models                  import BotConfig
from backend.bots.runner                import build_order
from backend.services.tradier_client    import TradierClient

logger = logging.getLogger("skystrike.schedulers")

def run_all():
    logger.info("Starting bot order submission process...")
    session = SessionLocal()
    client  = TradierClient()

    try:
        configs = session.query(BotConfig).filter(BotConfig.active == True).all()

        for cfg in configs:
            ticker = cfg.ticker

            # apply manual override if set
            if cfg.manual_override:
                contracts = cfg.override_contracts or cfg.contracts
                dte       = cfg.override_dte      or cfg.dte
            else:
                contracts = cfg.contracts
                dte       = cfg.dte

            # enforce minimum DTE of 1
            dte = max(dte, 1)

            # fallback confidence logic (if missing in schema)
            confidence = getattr(cfg, "confidence", 0.85)

            logger.info(f"Building order for {cfg.bot_name}: {ticker}, contracts={contracts}, dte={dte}, confidence={confidence}")

            try:
                order_spec = build_order(cfg.bot_name, ticker, contracts, dte, confidence)
                client.submit_order(order_spec)
                logger.info(f"? Order submitted for {cfg.bot_name}")
            except Exception as e:
                logger.error(f"? Error submitting order for {cfg.bot_name}: {e}")

    finally:
        session.close()

    logger.info("? Completed bot order submission process.")

if __name__ == "__main__":
    run_all()
