# backend/routes/__init__.py

import logging
import pkgutil
import importlib
from fastapi import APIRouter

logger = logging.getLogger(__name__)
router = APIRouter()

# Dynamically discover and include any submodule-level `router`
for _, module_name, _ in pkgutil.iter_modules(__path__):
    # skip non-endpoint modules
    if module_name == "schemas":
        continue

    module = importlib.import_module(f"{__name__}.{module_name}")
    if hasattr(module, "router"):
        logger.debug(f"Including routes from: {module_name}")
        router.include_router(module.router)

__all__ = ["router"]
