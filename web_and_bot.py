import os
from threading import Thread
from flask import Flask
from welcome_bot import get_application

app = Flask(__name__)

@app.route("/")
def index():
    return "OK", 200


def run_bot():
    application = get_application()
    print("Starting Telegram bot polling...")
    application.run_polling(stop_signals=None)


if __name__ == "__main__":
    # 1) Avvia Flask SUBITO (Render vede la porta)
    port = int(os.environ.get("PORT", 10000))
    print("Starting Flask on port", port)

    # 2) Avvia il bot in background
    bot_thread = Thread(target=run_bot, daemon=True)
    bot_thread.start()

    # 3) Flask resta il processo principale
    app.run(host="0.0.0.0", port=port)
