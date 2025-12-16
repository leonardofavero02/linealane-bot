import os
import asyncio
from flask import Flask
from welcome_bot import get_application

app = Flask(__name__)

@app.route("/")
def index():
    return "OK", 200


async def start_bot():
    application = get_application()
    print("Starting bot polling...")
    await application.initialize()
    await application.start()
    await application.bot.initialize()
    await application.updater.start_polling()


if __name__ == "__main__":
    # Avvia Flask SUBITO (Render contento)
    port = int(os.environ.get("PORT", 10000))
    print("Starting flask on port", port)

    loop = asyncio.get_event_loop()
    loop.create_task(start_bot())

    app.run(host="0.0.0.0", port=port)
