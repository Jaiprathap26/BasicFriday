import os
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from memory import get_all_recent

load_dotenv()

INCEPTION_API_KEY = os.getenv("INCEPTION_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"})

def morning_briefing():
    recent = get_all_recent(limit=5)
    context = ""
    if recent:
        context = "\n".join([f"{d} [{t}]: {c}" for d, t, c in recent])
        context = f"\n\nRecent logs from memory:\n{context}"
    
    prompt = f"""Give Jaiprathap a sharp morning briefing. Today is a new day.
    
Include:
1. One hard truth about where he stands right now
2. Top 3 priorities for today (PGCET, BrokerBot, career)
3. One motivational line — not soft, sharp like a coach

Keep it under 150 words. Start with "☀️ FRIDAY MORNING BRIEFING"{context}"""

    response = requests.post(
        'https://api.inceptionlabs.ai/v1/chat/completions',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {INCEPTION_API_KEY}',
        },
        json={
            "model": "mercury-2",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 300,
            "temperature": 0.8
        }
    )
    
    briefing = response.json()['choices'][0]['message']['content']
    send_telegram(briefing)
    print(f"[FRIDAY] Morning briefing sent.")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(morning_briefing, 'cron', hour=7, minute=0)
    scheduler.start()
    return scheduler