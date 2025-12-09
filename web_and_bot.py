# web_and_bot.py
import os
from flask import Flask
from threading import Thread
import time

from welcome_bot import get_application  # importa la factory

app = Flask(__name__)

@app.route("/")
def index():
    return "OK", 200

def run_bot():
    application = get_application()
    print("Starting bot polling...")  # questa riga appare nei logs
    try:
        application.run_polling(stop_signals=None)
    except Exception as e:
        print("Bot polling crashed:", e)
    print("Bot polling ended")

if __name__ == "__main__":
    # Start bot in background thread
    t = Thread(target=run_bot, daemon=True)
    t.start()

    # Small sleep so log ordering è più prevedibile
    time.sleep(0.2)

    port = int(os.environ.get("PORT", 10000))
    print("Starting flask on port", port)
    app.run(host="0.0.0.0", port=port)
