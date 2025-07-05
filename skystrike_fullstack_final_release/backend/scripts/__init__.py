# backend/scripts/__init__.py

import logging
import pkgutil
import importlib

logger = logging.getLogger(__name__)
__all__ = []

# Automatically import all Python modules in this package
for _, module_name, _ in pkgutil.iter_modules(__path__):
    # skip private or backup modules
    if module_name.startswith("_"):
        continue

    try:
        # import the module so its functions/entry-points are registered
        importlib.import_module(f"{__name__}.{module_name}")
        __all__.append(module_name)
        logger.debug(f"Loaded script module: {module_name}")
    except Exception as e:
        logger.error(f"Failed to import script module {module_name}: {e}")

# Now you can do:
#   from backend.scripts import apply_final_recommendation
#   from backend.scripts import backtest
# etc.
