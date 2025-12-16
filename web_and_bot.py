import os
from flask import Flask
from welcome_bot import get_application

app = Flask(__name__)

@app.route("/")
def index():
    return "OK", 200


if __name__ == "__main__":
    # Avvia bot Telegram
    application = get_application()
    print("Starting bot polling...")
    application.run_polling(stop_signals=None)

    # Avvia Flask (Render userà questo)
    port = int(os.environ.get("PORT", 10000))
    print("Starting flask on port", port)
    app.run(host="0.0.0.0", port=port)
