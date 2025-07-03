
# broker_link_ui.py

import logging
utils.database import get_user_broker, save_user_broker

class BrokerLinkManager:
    def __init__(self, user_id):
        self.user_id = user_id

    def get_broker(self):
        broker = get_user_broker(self.user_id)
        if not broker:
            logging.warning(f"[BrokerLink] No broker linked for user {self.user_id}")
        return broker

    def link_broker(self, broker_name, token, mode="paper"):
        if broker_name not in ["Tradier", "TastyTrade", "IBKR"]:
            raise ValueError(f"Unsupported broker: {broker_name}")
        config = {
            "broker": broker_name,
            "token": token,
            "mode": mode
        }
        save_user_broker(self.user_id, config)
        logging.info(f"[BrokerLink] Linked {broker_name} for user {self.user_id}")
        return config
