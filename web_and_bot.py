# web_and_bot.py
import os
from flask import Flask
from threading import Thread
import time

# IMPORT application factory dal tuo welcome_bot.py
from welcome_bot import get_application

app = Flask(__name__)

@app.route("/")
def index():
    return "ok", 200

def run_bot():
    application = get_application()
    print("Starting bot polling...")              # <<-- controllo visibile nei logs
    try:
        application.run_polling(stop_signals=None)  # blocca il thread ma non la main
    except Exception as e:
        print("Bot polling crashed:", e)
    print("Bot polling ended")

if __name__ == "__main__":
    # Avvia il polling in un thread demon
    t = Thread(target=run_bot, daemon=True)
    t.start()

    # Attendi qualche decina di ms per vedere la print del thread nei logs
    time.sleep(0.2)

    port = int(os.environ.get("PORT", 10000))
    print("Starting flask on port", port)
    app.run(host="0.0.0.0", port=port)
