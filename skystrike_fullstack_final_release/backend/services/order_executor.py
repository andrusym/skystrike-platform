# services/order_executor.py

import traceback
from datetime import datetime
from fastapi.responses import JSONResponse
services.tradier_api import place_order
services.log_writer import append_log

async def execute_order(order_payload: dict, bot_name: str, ticker: str, contracts: int):
    """
    Submits a fully-formed order payload to Tradier and logs the result.
    
    Args:
        order_payload (dict): Tradier-formatted order
        bot_name (str): Strategy name (e.g., "Iron Condor")
        ticker (str): Underlying ticker
        contracts (int): Contract count

    Returns:
        dict: Standardized response
    """
    try:
        print(f"?? Executing order for {bot_name} on {ticker}")
        print(f"?? Payload: {order_payload}")

        response = await place_order(order_payload)

        if isinstance(response, JSONResponse):
            response_body = response.body.decode() if hasattr(response, "body") else str(response)
            result = {
                "status": "error",
                "bot": bot_name,
                "ticker": ticker,
                "contracts": contracts,
                "broker_response": {
                    "error": response_body
                }
            }
        elif isinstance(response, dict) and "error" in response:
            result = {
                "status": "error",
                "bot": bot_name,
                "ticker": ticker,
                "contracts": contracts,
                "broker_response": response
            }
        else:
            result = {
                "status": "order submitted",
                "bot": bot_name,
                "ticker": ticker,
                "contracts": contracts,
                "broker_response": response
            }

        # Log every attempt regardless of result
        append_log({
            "timestamp": datetime.utcnow().isoformat(),
            "bot": bot_name,
            "ticker": ticker,
            "contracts": contracts,
            "order": order_payload,
            "response": result
        })

        return result

    except Exception as e:
        print(f"? Exception in execute_order(): {str(e)}")
        traceback.print_exc()
        return {
            "status": "error",
            "bot": bot_name,
            "ticker": ticker,
            "contracts": contracts,
            "broker_response": {
                "error": str(e)
            }
        }
