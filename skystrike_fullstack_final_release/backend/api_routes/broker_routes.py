from fastapi import APIRouter, Query
from tradier_client import tradier_get

router = APIRouter()

@router.get("/account")
def get_account():
        return tradier_get("user/profile")
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.get("/positions")
def get_positions():
        return tradier_get("accounts/{account_id}/positions")  # account_id needs to be dynamically inserted
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.get("/quote")
def get_quote(symbol: str = Query(...)):
        return tradier_get("markets/quotes", params={"symbols": symbol})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
