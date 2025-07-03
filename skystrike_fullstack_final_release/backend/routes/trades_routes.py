
from fastapi import APIRouter
import sqlite3
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/api/trades")
def get_trades():
    try:
        conn = sqlite3.connect("skystrike.db")
        cursor = conn.cursor()
        cursor.execute("SELECT symbol, strategy, status, pnl, opened_at, closed_at FROM trades")
        rows = cursor.fetchall()
        conn.close()
        result = []
        for row in rows:
            result.append({
                "symbol": row[0],
                "strategy": row[1],
                "status": row[2],
                "pnl": row[3],
                "opened_at": row[4],
                "closed_at": row[5],
            })
        return result
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
