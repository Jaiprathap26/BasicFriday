import os
import requests
from dotenv import load_dotenv

load_dotenv()
INCEPTION_API_KEY = os.getenv("INCEPTION_API_KEY")

COACH_PROMPT = """You are Jaiprathap's brutally honest career coach.

You specialize in:
- AI engineering roadmap advice
- Study plans for PGCET (exam date: May 24)
- GitHub and LinkedIn strategy
- BrokerBot SaaS launch strategy

Rules:
- No fluff. No sympathy. Only action.
- If he's on track, confirm it and push harder.
- If he's off track, call it out with specific numbers.
- Always end with ONE clear next action."""

def coach_reply(user_message: str) -> str:
    response = requests.post(
        'https://api.inceptionlabs.ai/v1/chat/completions',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {INCEPTION_API_KEY}',
        },
        json={
            "model": "mercury-2",
            "messages": [
                {"role": "system", "content": COACH_PROMPT},
                {"role": "user", "content": user_message}
            ],
            "max_tokens": 500,
            "temperature": 0.6
        }
    )
    return response.json()['choices'][0]['message']['content']