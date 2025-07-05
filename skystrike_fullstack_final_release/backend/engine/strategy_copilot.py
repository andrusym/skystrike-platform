import os
import openai
import logging

openai.api_key = os.getenv("OPENAI_API_KEY", "")

class StrategyCopilot:
    def __init__(self, prompt_prefix: str = "Generate a defined-risk options strategy for:"):
        self.prompt_prefix = prompt_prefix

    def generate_strategy(self, user_query: str) -> str:
        try:
            full_prompt = f"{self.prompt_prefix} {user_query}"
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert options trading assistant."},
                    {"role": "user",   "content": full_prompt}
                ],
                temperature=0.4,
                max_tokens=400
            )
            strategy_text = response.choices[0].message.content.strip()
            logging.info(f"[StrategyCopilot] Generated strategy for prompt: '{user_query}'")
            return strategy_text
        except Exception as e:
            logging.error(f"[StrategyCopilot] Failed to generate strategy: {e}")
            return f"Error: {e}"
