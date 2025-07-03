from backend.utils.database import get_strategy_config, save_strategy_config


def load_strategy_config():
    """
    Load the full strategy configuration dict.
    """
    return get_strategy_config()


def persist_strategy_config(config):
    """
    Save updated strategy configuration.
    """
    save_strategy_config(config)
