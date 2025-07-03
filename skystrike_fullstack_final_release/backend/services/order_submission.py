import json
import logging
import os
from typing import Dict

from backend.bots.runner import build_order
from backend.services.tradier_client import TradierClient

# Paths (adjust as necessary)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
BOT_CONFIG_PATH = os.path.join(BASE_DIR, 'config', 'bot_config.json')
TRADE_LOG_PATH = os.path.join(BASE_DIR, 'logs', 'trade_log.json')

client = TradierClient()

def _load_bot_config():
    with open(BOT_CONFIG_PATH) as f:
        raw = json.load(f)
    # Handle dict or list
    if isinstance(raw, dict):
        entries = []
        for bot_name, entry in raw.items():
            if not isinstance(entry, dict):
                continue
            entry_copy = entry.copy()
            entry_copy['bot'] = bot_name
            entries.append(entry_copy)
        return entries
    elif isinstance(raw, list):
        return raw
    else:
        raise ValueError("bot_config.json must be a dict or list")

def _append_trade_log(entry: Dict):
    os.makedirs(os.path.dirname(TRADE_LOG_PATH), exist_ok=True)
    if os.path.exists(TRADE_LOG_PATH):
        with open(TRADE_LOG_PATH) as f:
            logs = json.load(f)
    else:
        logs = []
    logs.append(entry)
    with open(TRADE_LOG_PATH, 'w') as f:
        json.dump(logs, f, indent=2)

def run():
    logging.info("Loading bot configuration...")
    config_entries = _load_bot_config()
    for bot_entry in config_entries:
        bot_name = bot_entry.get('bot')
        ticker = bot_entry.get('ticker')
        contracts = bot_entry.get('contracts', 0)
        dte = bot_entry.get('dte', 0)
        active = bot_entry.get('active', False)

        if not active or contracts <= 0:
            logging.debug(f"Skipping {bot_name} (active={active}, contracts={contracts})")
            continue

        logging.info(f"Building order for {bot_name}: {ticker}, contracts={contracts}, dte={dte}")
        try:
            order_spec = build_order(bot_name, ticker, contracts, dte)
            logging.info(f"Submitting order for {bot_name}: {order_spec}")
            result = client.submit_order(order_spec)
            _append_trade_log({
                'bot': bot_name,
                'ticker': ticker,
                'contracts': contracts,
                'dte': dte,
                'order_spec': order_spec,
                'result': result
            })
        except Exception as e:
            logging.error(f"Error submitting order for {bot_name}: {e}")
            _append_trade_log({
                'bot': bot_name,
                'ticker': ticker,
                'error': str(e)
            })
