
# broker_link_registry.py

import logging
utils.database import get_broker_config, save_broker_config

class BrokerLinkRegistry:
    def __init__(self, user_id):
        self.user_id = user_id
        self.supported_brokers = ["Tradier", "TastyTrade", "IBKR"]

    def register(self, broker_name, api_token, mode="paper"):
        if broker_name not in self.supported_brokers:
            raise ValueError(f"Unsupported broker: {broker_name}")

        config = {
            "user_id": self.user_id,
            "broker": broker_name,
            "api_token": api_token,
            "mode": mode
        }

        save_broker_config(self.user_id, config)
        logging.info(f"[BrokerRegistry] Registered {broker_name} for user {self.user_id}")

    def get_broker(self):
        config = get_broker_config(self.user_id)
        if not config:
            logging.warning(f"[BrokerRegistry] No broker linked for user {self.user_id}")
        return config
