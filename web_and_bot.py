# web_and_bot.py
import os
import threading
import signal
import sys
from flask import Flask
from telegram.ext import ApplicationBuilder, MessageHandler, filters

# --- Config ---
TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TOKEN:
    print("ERROR: TELEGRAM_TOKEN env var not set")
    sys.exit(1)

PORT = int(os.environ.get("PORT", 8080))  # Render sets PORT for web services

# --- Small web app (necessary per Render port scan) ---
app = Flask(__name__)

@app.route("/")
def index():
    return "OK - bot running"

# --- Telegram bot handlers ---
async def on_message(update, context):
    text = update.message.text if update.message else "<no message>"
    print("Received:", text)

def run_bot():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.ALL, on_message))
    application.run_polling(stop_signals=None)

def handle_exit(signum, frame):
    print("Shutting down")
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_exit)
signal.signal(signal.SIGINT, handle_exit)

if __name__ == "__main__":
    t = threading.Thread(target=run_bot, daemon=True)
    t.start()
    app.run(host="0.0.0.0", port=PORT)
