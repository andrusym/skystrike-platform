# backend/routes/debug_routes.py

from fastapi import FastAPI
from backend.routes.login_routes import router as login_router

app = FastAPI()
app.include_router(login_router, prefix="/api")

# Debug route printer
@app.get("/debug/routes")
def list_routes():
    return [
        {
            "path": route.path,
            "name": route.name,
            "methods": list(route.methods),
        }
        for route in app.routes
    ]
