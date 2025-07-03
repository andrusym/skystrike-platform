from fastapi import FastAPI
from routes import router as api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="SkyStrike Trading Platform",
    description="Refactored backend with full paper/live trading support",
    version="1.0.0"
)

# CORS settings (allow all for now; restrict in production if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount all API routes under /api
app.include_router(api_router, prefix="/api")
