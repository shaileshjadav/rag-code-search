import requests
import os

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/embeddings"
MODEL = "openai/text-embedding-ada-002"  # cheap + good for code search

def get_embedding(text: str):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "input": text
    }

    resp = requests.post(OPENROUTER_BASE_URL, headers=headers, json=payload)

    if resp.status_code != 200:
        print("❌ Error from OpenRouter:", resp.status_code, resp.text)
        return None

    try:
        data = resp.json()
        return data["data"][0]["embedding"]
    except Exception as e:
        print("❌ JSON decode error:", e, " Response:", resp.text[:200])
        return None
