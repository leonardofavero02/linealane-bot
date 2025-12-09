# web_and_bot.py
import os
import threading
import signal
import sys
from flask import Flask
from telegram.ext import ApplicationBuilder, MessageHandler, filters

# --- Config: accetta sia BOT_TOKEN che TELEGRAM_TOKEN ---
TOKEN = os.environ.get("BOT_TOKEN") or os.environ.get("TELEGRAM_TOKEN")
if not TOKEN:
    print("ERROR: BOT_TOKEN or TELEGRAM_TOKEN not set")
    sys.exit(1)

PORT = int(os.environ.get("PORT", 8080))

# --- Mini web server per Render ---
app = Flask(__name__)

@app.route("/")
def index():
    return "Bot running"

# --- Handler di debug: stampa i messaggi ---
async def on_message(update, context):
    text = update.message.text if update.message else "<no text>"
    print("Received:", text)

def run_bot():
    application = ApplicationBuilder().token(TOKEN).build()

    # Logga TUTTI i messaggi (utile per verificare che funziona)
    application.add_handler(MessageHandler(filters.ALL, on_message))

    application.run_polling(stop_signals=None)

def handle_exit(signum, frame):
    print("Shutting down...")
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_exit)
signal.signal(signal.SIGINT, handle_exit)

if __name__ == "__main__":
    # Bot in background
    t = threading.Thread(target=run_bot, daemon=True)
    t.start()

    # Server web richiesto da Render
    app.run(host="0.0.0.0", port=PORT)
