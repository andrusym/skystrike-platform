# backend/main.py

import logging
from typing import List, Literal

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings

# Import the config router here
from backend.routes.config_routes import router as config_router

class Settings(BaseSettings):
    ENV: str = "production"
    APP_NAME: str = "SkyStrike API"
    VERSION: str = "1.0.0"
    PORT: int = 8000
    LOG_LEVEL: str = "INFO"

    # Allowed hosts—add dev hosts here
    ALLOWED_HOSTS: List[str] = ["yourdomain.com", "localhost", "127.0.0.1"]
    CORS_ORIGINS: List[AnyHttpUrl] = ["https://yourdomain.com"]

    # Tradier credentials
    TRADIER_MODE: Literal["paper", "live"] = "paper"
    TRADIER_PAPER_ACCESS_TOKEN: str
    TRADIER_PAPER_ACCOUNT_ID: str
    TRADIER_LIVE_ACCESS_TOKEN: str
    TRADIER_LIVE_ACCOUNT_ID: str

    # JWT settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)
logger = logging.getLogger(settings.APP_NAME)

app = FastAPI(title=settings.APP_NAME, version=settings.VERSION)

# Middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(o) for o in settings.CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Authorization", "Content-Type"],
)

# Auth dependency
from backend.dependencies.auth import get_current_user

# Core routers
from backend.routes.order_routes import router as order_router
from backend.routes.login_routes           import router as login_router
from backend.routes.dashboard_routes       import router as dashboard_router
from backend.routes.trade_routes           import router as trades_router
from backend.routes.bots_status_routes     import router as bots_status_router
from backend.routes.wealth_routes          import router as wealth_router
from backend.routes.order_routes           import router as order_router
from backend.routes.api_orders_history     import router as orders_history_router
from backend.routes.portfolio_final_routes import router as portfolio_final_router
from backend.routes.ml_routes              import router as ml_router
from backend.routes.risk_routes            import router as risk_router
from backend.routes.setup_routes           import router as setup_router
from backend.routes.admin_routes           import router as admin_router
from backend.routes.portfolio_apply_route  import router as apply_router
from backend.routes.bot_trigger_dynamic    import router as bot_trigger_router
from backend.routes.bots_log_route         import router as bots_log_router
from backend.routes.replication_routes     import router as replication_router
from backend.routes.wealth_holdings_route  import router as holdings_router
from backend.routes.wealth_log_route       import router as wealth_log_router
from backend.routes.order_status_routes    import router as order_status_router
from backend.routes.lifecycle_routes       import router as lifecycle_router
from backend.routes.fallback_routes        import router as fallback_router
from backend.routes.sizing_preview_route   import router as sizing_preview_router
from backend.routes.config_log_route       import router as config_log_router

# Optional routers
from backend.routes.api_positions          import router as positions_router
from backend.routes.api_copilot            import router as copilot_router
from backend.routes.webhook_listener       import router as webhook_router

# Startup/shutdown events
@app.on_event("startup")
async def on_startup():
    logger.info("Application startup complete")

@app.on_event("shutdown")
async def on_shutdown():
    logger.info("Application shutdown complete")

# Auth + health
app.include_router(login_router, prefix="/api", tags=["auth"])
app.include_router(config_router)

@app.get("/api/health", dependencies=[Depends(get_current_user)], tags=["health"])
async def health_check():
    return {"status": "ok"}

# Core API routes
app.include_router(dashboard_router,       prefix="/api", tags=["dashboard"])
app.include_router(trades_router,          prefix="/api", tags=["trades"])
app.include_router(bots_status_router,     prefix="/api", tags=["bots_status"])
app.include_router(wealth_router,          prefix="/api", tags=["wealth"])
app.include_router(order_router)  # /api/orders is set inside order_routes.py

# Mount orders history under /api/orders/history
app.include_router(
    orders_history_router,
    prefix="/api/orders",
    tags=["orders_history"]
)

app.include_router(portfolio_final_router, prefix="/api", tags=["portfolio_final"])
app.include_router(ml_router,              prefix="/api", tags=["ml"])
app.include_router(risk_router,            prefix="/api", tags=["risk"])
app.include_router(setup_router,           prefix="/api", tags=["setup"])
app.include_router(admin_router,           prefix="/api", tags=["admin"])
app.include_router(apply_router,           prefix="/api", tags=["portfolio_apply"])
app.include_router(bot_trigger_router,     prefix="/api", tags=["bot_trigger"])
app.include_router(bots_log_router,        prefix="/api", tags=["bots_log"])
app.include_router(replication_router,     prefix="/api", tags=["replication"])
app.include_router(holdings_router,        prefix="/api", tags=["wealth_holdings"])
app.include_router(wealth_log_router,      prefix="/api", tags=["wealth_log"])
app.include_router(order_status_router,    prefix="/api", tags=["order_status"])
app.include_router(lifecycle_router,       prefix="/api", tags=["lifecycle"])
app.include_router(fallback_router,        prefix="/api", tags=["fallbacks"])
app.include_router(sizing_preview_router,  prefix="/api", tags=["sizing_preview"])
app.include_router(config_log_router,      prefix="/api", tags=["config_log"])

# Optional routes
app.include_router(positions_router,       prefix="/api", tags=["positions"])
app.include_router(copilot_router,         prefix="/api", tags=["copilot"])
app.include_router(webhook_router,         prefix="/api", tags=["webhook"])

# Run via Uvicorn if invoked directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=settings.PORT,
        log_level=settings.LOG_LEVEL.lower(),
    )