
# strategy_copilot.py

import openai
import logging
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

class StrategyCopilot:
    def __init__(self, prompt_prefix="Generate a defined-risk options strategy for:"):
        self.prompt_prefix = prompt_prefix

    def generate_strategy(self, user_query):
        try:
            full_prompt = f"{self.prompt_prefix} {user_query}"
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert options trading assistant."},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=0.4,
                max_tokens=400
            )
            strategy_text = response['choices'][0]['message']['content'].strip()
            logging.info(f"[StrategyCopilot] Generated strategy for prompt: '{user_query}'")
            return strategy_text
        except Exception as e:
            logging.error(f"[StrategyCopilot] Failed to generate strategy: {e}")
            return f"Error: {e}"
