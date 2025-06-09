from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount built frontend from ./dist/
dist_path = Path(__file__).parent / "dist"
app.mount("/", StaticFiles(directory=dist_path, html=True), name="static")

@app.get("/dashboard")
def get_dashboard():
    return {
        "daily_pl": 1380.45,
        "weekly_target": 5000,
        "active_capital": 75000,
        "strategies": [
            {"name": "Iron Condor", "ticker": "SPX", "dte": 0, "contracts": 12, "pnl": 450.75, "ml_score": 0.91, "status": "active"},
            {"name": "King Condor", "ticker": "NDX", "dte": 1, "contracts": 8, "pnl": 320.10, "ml_score": 0.76, "status": "active"},
            {"name": "GapStat", "ticker": "QQQ", "dte": 0, "contracts": 5, "pnl": 170.35, "ml_score": 0.82, "status": "active"}
        ]
    }