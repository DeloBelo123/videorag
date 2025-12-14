import os
import httpx

from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY is not set")

r = httpx.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    },
    json={
        "model": "openai/gpt-4o-mini",
        "messages": [
            {"role": "user", "content": "whats up ma g?"}
        ],
        "max_tokens": 5
    },
    timeout=10
)

print(r.status_code)
print(r.json())
