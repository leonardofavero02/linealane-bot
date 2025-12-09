import os
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.environ.get("BOT_TOKEN")

WELCOME_MESSAGE = (
    "‼️💬 Benvenuto/a {first_name} nel gruppo Linea Lane!\n\n"
    "📘 Codice di Condotta:\n"
    "<a href=\"https://telegra.ph/Reg-Community-08-29\">Regole della Community</a>\n\n"
    "⚪🔴 Partecipa con rispetto.\n"
    "Ricorda che sei parte della nostra community!"
)

# dedupe semplice per evitare doppi invii
_recent_welcomes = {}
def seen_recently(chat_id: int, user_id: int, ttl: int = 30) -> bool:
    key = (chat_id, user_id)
    now = time.time()
    for k, ts in list(_recent_welcomes.items()):
        if now - ts > ttl:
            _recent_welcomes.pop(k, None)
    if key in _recent_welcomes:
        return True
    _recent_welcomes[key] = now
    return False

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_message or not update.effective_message.new_chat_members:
        return
    chat = update.effective_chat
    for member in update.effective_message.new_chat_members:
        if seen_recently(chat.id, member.id):
            continue
        text = WELCOME_MESSAGE.format(first_name=member.first_name or member.full_name or "amico")
        await context.bot.send_message(
            chat.id,
            text,
            parse_mode="HTML",
            disable_web_page_preview=True
        )

def main():
    if not BOT_TOKEN:
        raise SystemExit("BOT_TOKEN non impostato. Aggiungilo come variabile d'ambiente.")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    app.run_polling()

if __name__ == "__main__":
    main()

