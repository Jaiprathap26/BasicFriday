import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from memory import init_db, save_memory, get_memories, get_all_recent
from scheduler import start_scheduler, morning_briefing

load_dotenv()

init_db()

INCEPTION_API_KEY = os.getenv("INCEPTION_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

SYSTEM_PROMPT = """You are FRIDAY — Jaiprathap's personal AI OS.

You know his goals:
- Build AI engineering career (Mercury 2 + LangChain + CrewAI + FastAPI)
- Crack PGCET exam on May 24
- Get first freelance income by end of May
- Build BrokerBot SaaS — WhatsApp AI for real estate brokers
- Post on LinkedIn daily
- Push to GitHub daily

His stack: Mercury 2, CrewAI, LangChain, FastAPI, Python, PostgreSQL
His current status: BCA graduate, 20+ GitHub projects, former backend intern at Gowri Software

Rules:
- Be direct. Be his coach. Push him when he's slacking.
- Never sugarcoat. Never say "great question".
- Sound like a sharp colleague, not a chatbot.
- Keep replies under 200 words unless he asks for a full plan.
- When he says "log: ..." acknowledge it and tell him to keep going.
- When he says "i feel like giving up" — snap him back with facts, not sympathy."""

conversation_history = []


def ask_friday(user_message: str) -> str:
    conversation_history.append({"role": "user", "content": user_message})

    response = requests.post(
        'https://api.inceptionlabs.ai/v1/chat/completions',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {INCEPTION_API_KEY}',
        },
        json={
            "model": "mercury-2",
            "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history[-6:],
            "max_tokens": 1000,
            "temperature": 0.7
        }
    )

    reply = response.json()['choices'][0]['message']['content']
    conversation_history.append({"role": "assistant", "content": reply})
    return reply


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    print(f"[{update.effective_user.first_name}]: {user_msg}")

    # auto-save logs when user says "log: ..."
    if user_msg.lower().startswith("log:"):
        save_memory("match_log", user_msg[4:].strip())

    # if asking about history, pull from memory and re-ask
    if "how was my week" in user_msg.lower() or "last week" in user_msg.lower():
        logs = get_memories("match_log", limit=7)
        if logs:
            memory_text = "\n".join([f"{d}: {c}" for d, c in logs])
            reply = ask_friday(f"summarize these match logs for me:\n{memory_text}")
        else:
            reply = ask_friday(user_msg)
    else:
        reply = ask_friday(user_msg)

    print(f"[FRIDAY]: {reply}")
    await update.message.reply_text(reply)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("FRIDAY online. what do you need?")


async def brief_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    morning_briefing()
    await update.message.reply_text("briefing triggered — check above.")


def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("brief", brief_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    start_scheduler()
    print("FRIDAY is online. Ctrl+C to stop.")
    print("Scheduler started — morning briefing at 7am daily.")

    app.run_polling()


if __name__ == "__main__":
    main()