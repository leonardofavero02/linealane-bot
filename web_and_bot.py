# web_and_bot.py
import os
import threading
import signal
import sys
import time
import httpx
from flask import Flask
from telegram.ext import ApplicationBuilder, MessageHandler, filters

# TOKEN: legge BOT_TOKEN (primario) o TELEGRAM_TOKEN (fallback)
TOKEN = os.environ.get("BOT_TOKEN") or os.environ.get("TELEGRAM_TOKEN")
if not TOKEN:
    print("ERROR: BOT_TOKEN or TELEGRAM_TOKEN not set")
    sys.exit(1)

PORT = int(os.environ.get("PORT", 10000))

app = Flask(__name__)

@app.route("/")
def index():
    return "Bot running"

# prova a importare handler di welcome
has_welcome = False
try:
    from welcome_bot import welcome
    has_welcome = True
    print("Imported welcome handler from welcome_bot.py")
except Exception as e:
    print("Could not import welcome handler (ok if absent):", e)

# cancella eventuale webhook residuo (evita conflitti)
def delete_webhook_if_exists():
    try:
        resp = httpx.post(f"https://api.telegram.org/bot{TOKEN}/deleteWebhook", timeout=10.0)
        print("deleteWebhook response:", resp.status_code, resp.text[:200])
    except Exception as e:
        print("deleteWebhook failed:", e)

# logger fallback per ogni update (utile per debug)
async def on_message(update, context):
    text = None
    if update.message and update.message.text:
        text = update.message.text
    print(f"Received: {text}")

def run_bot():
    delete_webhook_if_exists()
    application = ApplicationBuilder().token(TOKEN).build()

    # registra handler welcome per nuovi membri
    if has_welcome:
        from telegram.ext import MessageHandler as MH
        from telegram.ext import filters as F
        application.add_handler(MH(F.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
        print("Registered NEW_CHAT_MEMBERS -> welcome")

    # fallback logger (tuttti gli update)
    application.add_handler(MessageHandler(filters.ALL, on_message))

    # run polling (non usare stop_signals per evitare conflitti con thread)
    application.run_polling(stop_signals=None)

def handle_exit(signum, frame):
    print("Shutting down...")
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_exit)
signal.signal(signal.SIGINT, handle_exit)

if __name__ == "__main__":
    t = threading.Thread(target=run_bot, daemon=True)
    t.start()
    # piccola pausa per permettere al thread di avviarsi
    time.sleep(0.5)
    # avvia flask sull porta definita da Render (10000)
    app.run(host="0.0.0.0", port=PORT)
