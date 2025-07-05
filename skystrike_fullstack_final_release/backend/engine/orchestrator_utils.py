import importlib
import pkgutil
import logging

logger = logging.getLogger(__name__)

def safe_submodules(package_name: str) -> list[str]:
    """
    Return a list of submodule names under a package,
    or an empty list if it's a flat module.
    """
    try:
        module = importlib.import_module(package_name)
        if not hasattr(module, "__path__"):
            logger.warning(f"{package_name} is not a package — skipping submodule scan.")
            return []
        return [name for _, name, _ in pkgutil.iter_modules(module.__path__)]
    except Exception as e:
        logger.error(f"Failed to scan submodules in {package_name}: {e}")
        return []
