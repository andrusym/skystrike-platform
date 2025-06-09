
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router as api_router

app = FastAPI(
    title="SkyStrike Trading Platform",
    description="Phase 1 Production Build - Automated Options Trading",
    version="7.0.0"
)

# CORS settings for frontend communication
origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://staging.skystrike.ai"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routes
app.include_router(api_router)

@app.get("/")
def root():
    return {
        "message": "SkyStrike backend is live.",
        "endpoints": ["/health", "/dashboard", "/trade/start"]
    }
