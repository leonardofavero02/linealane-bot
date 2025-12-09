import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

WELCOME_MESSAGE = (
    "‼️💬 Benvenuto/a {first_name} nel gruppo Linea Lane!\n\n"
    "📘 Codice di Condotta:\n"
    "<a href=\"https://telegra.ph/Reg-Community-08-29\">Regole della Community</a>\n\n"
    "⚪🔴 Partecipa con rispetto.\n"
    "Ricorda che sei parte della nostra community!"
)

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:  # Messaggi strani / system
        return

    user = update.message.from_user
    if user is None:
        return

    # Solo quando qualcuno entra nel gruppo
    if update.message.new_chat_members:
        for member in update.message.new_chat_members:
            await update.message.reply_html(
                WELCOME_MESSAGE.format(first_name=member.first_name)
            )

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    app.run_polling()

if __name__ == "__main__":
    main()
