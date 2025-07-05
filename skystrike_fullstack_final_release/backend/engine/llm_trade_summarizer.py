import openai
import os
from datetime import datetime

openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_trade(bot, ticker, contracts, dte, confidence, rationale=None):
    prompt = f"""
You are a professional options trading assistant.
Summarize the reason behind this trade in clear, human terms:

- Bot: {bot}
- Ticker: {ticker}
- Contracts: {contracts}
- DTE: {dte}
- Confidence: {confidence}
- ML Rationale: {rationale or 'N/A'}

Respond with 1–2 bullet points of rationale.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=150
        )
        summary = response.choices[0].message.content.strip()
        return {
            "bot": bot,
            "ticker": ticker,
            "summary": summary,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {"error": str(e), "bot": bot, "ticker": ticker}