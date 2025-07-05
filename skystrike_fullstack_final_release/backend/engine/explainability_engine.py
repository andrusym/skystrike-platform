import json

ML_PATH = "data/ml_scores.json"
METADATA_PATH = "data/bot_metadata.json"

def get_explanation(bot_ticker: str):
    try:
        with open(ML_PATH, "r") as f:
            ml_data = json.load(f)
        with open(METADATA_PATH, "r") as f:
            meta = json.load(f)
    except:
        return {"error": "data load failed"}

    bot_data = ml_data.get(bot_ticker, {})
    bot_name, ticker = bot_ticker.split(":")

    score = bot_data.get("confidence", 0)
    contracts = bot_data.get("contracts", 0)
    rationale = bot_data.get("rationale", "")
    cooldown = bot_data.get("cooldown", False)
    fallback = bot_data.get("fallback_active", False)

    meta_info = meta.get(bot_name, {})
    base_strategy = meta_info.get("strategy_type", "undefined")
    typical_dte = meta_info.get("default_dte", "N/A")
    risk_profile = meta_info.get("risk_profile", "moderate")

    return {
        "bot": bot_name,
        "ticker": ticker,
        "confidence": score,
        "contracts": contracts,
        "cooldown": cooldown,
        "fallback_active": fallback,
        "strategy_type": base_strategy,
        "default_dte": typical_dte,
        "risk_profile": risk_profile,
        "rationale": rationale or "ML score + capital + risk profile aligned"
    }