import os
import requests
from dotenv import load_dotenv

load_dotenv()
INCEPTION_API_KEY = os.getenv("INCEPTION_API_KEY")

DOUBT_PROMPT = """You are a senior AI engineer and full-stack developer.

Jaiprathap asks you technical questions. Answer like a senior colleague, not a tutor.

Rules:
- Give working code examples when relevant
- Explain the WHY, not just the what
- If it's a bug, diagnose it fast and give the fix
- Stack: Python, FastAPI, LangChain, Mercury 2, PostgreSQL, Telegram Bot API"""

def solve_doubt(user_message: str) -> str:
    response = requests.post(
        'https://api.inceptionlabs.ai/v1/chat/completions',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {INCEPTION_API_KEY}',
        },
        json={
            "model": "mercury-2",
            "messages": [
                {"role": "system", "content": DOUBT_PROMPT},
                {"role": "user", "content": user_message}
            ],
            "max_tokens": 800,
            "temperature": 0.5
        }
    )
    return response.json()['choices'][0]['message']['content']