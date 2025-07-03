
# wealth_config.py

import logging
utils.database import get_wealth_settings, save_wealth_settings

class WealthEngineConfig:
    def __init__(self, user_id):
        self.user_id = user_id

    def get_settings(self):
        settings = get_wealth_settings(self.user_id)
        if not settings:
            logging.warning(f"[WealthConfig] No wealth settings found for user {self.user_id}")
        return settings

    def update_settings(self, updates):
        current = get_wealth_settings(self.user_id) or {}
        updated = {**current, **updates}
        save_wealth_settings(self.user_id, updated)
        logging.info(f"[WealthConfig] Updated wealth settings for user {self.user_id}")
        return updated
