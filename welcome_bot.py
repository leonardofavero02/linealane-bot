from telegram import Update, Chat
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "8411027702:AAGhAN6xe72YBD5mIUcHgzht7PWJ25y5uN8"

WELCOME_MESSAGE = (
    "‼️💬 Benvenuto {first_name} nel gruppo Linea Lane!\n\n"
    "📘 Codice di Condotta:\n"
    "https://telegra.ph/Reg-Community-08-29\n\n"
    "⚖️ Informativa Legale:\n"
    "https://telegra.ph/Inf-legale-08-29\n\n"
    "🔴⚪ Partecipa con rispetto.\n"
    "Ricorda che sei parte della nostra community!"
)async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    for member in update.effective_message.new_chat_members:
        text = WELCOME_MESSAGE.format(first_name=member.first_name)
        await context.bot.send_message(chat.id, text)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    app.run_polling()

if __name__ == "__main__":
    main()

