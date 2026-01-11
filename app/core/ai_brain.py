import os
import httpx

class SentinelBrain:
    def __init__(self):
        # We only need the OpenRouter key now
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.url = "https://openrouter.ai/api/v1/chat/completions"

    def ask(self, system_prompt, user_message):
        # We use Llama 3.3 70B (Free) for high-end reasoning
        model = "meta-llama/llama-3.3-70b-instruct:free"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "http://localhost:8000", # Optional for OpenRouter
        }

        json_data = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        }

        try:
            # Using httpx for the API call
            with httpx.Client() as client:
                response = client.post(self.url, headers=headers, json=json_data, timeout=60.0)
                response.raise_for_status()
                return response.json()['choices'][0]['message']['content']
        except Exception as e:
            return f"Error: {str(e)}"