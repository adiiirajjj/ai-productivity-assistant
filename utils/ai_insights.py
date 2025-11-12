from dotenv import load_dotenv
load_dotenv()

import os, requests

OPENROUTER_KEY = os.getenv("OPENROUTER_KEY", "")

def get_ai_insight(prompt: str):
    """Generate insight via free OpenRouter API"""
    if not OPENROUTER_KEY:
        return "⚠️ Missing OpenRouter key."

    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "HTTP-Referer": "http://localhost:8000",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistralai/mistral-7b-instruct",  # free public model
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        r = requests.post("https://openrouter.ai/api/v1/chat/completions",
                          headers=headers, json=payload, timeout=30)
        if r.status_code == 200:
            data = r.json()
            return data["choices"][0]["message"]["content"].strip()
        else:
            return f"⚠️ API Error {r.status_code}: {r.text[:120]}"
    except Exception as e:
        return f"❌ Error: {str(e)}"
