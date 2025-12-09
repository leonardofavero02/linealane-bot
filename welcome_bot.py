# welcome_bot.py
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    # non lanciare eccezione qui se vuoi che import non fallisca;
    # ma è utile per debug locale
    raise RuntimeError("BOT_TOKEN env var not set")

WELCOME_MESSAGE = (
    "‼️💬 Benvenuto/a {first_name} nel gruppo Linea Lane!\n\n"
    
    "📘 Codice di Condotta:\n"
    "<a href=\"https://telegra.ph/Reg-Community-08-29\">Regole della Community</a>\n\n"
    
    "🌐 Social:\n"
    "Instagram: <a href=\"https://www.instagram.com/linea_lane/\">https://www.instagram.com/linea_lane/</a>\n"
    "Facebook: <a href=\"https://www.facebook.com/DirettaLineaLane\">https://www.facebook.com/DirettaLineaLane</a>\n"
    "YouTube: <a href=\"https://www.youtube.com/@linealane\">https://www.youtube.com/@linealane</a>\n"
    "TikTok: <a href=\"https://www.tiktok.com/@linea_lane\">https://www.tiktok.com/@linea_lane</a>\n\n"
    
    "⚪🔴 Partecipa con rispetto.\n"
    "Ricorda che sei parte della nostra community!"
)


async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return

    if update.message.new_chat_members:
        for member in update.message.new_chat_members:
            first = member.first_name or member.full_name or "amico/a"
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=WELCOME_MESSAGE.format(first_name=first),
                parse_mode="HTML",
                disable_web_page_preview=True
            )

def get_application():
    """Return a built telegram.ext.Application ready to run_polling()."""
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    return app

# Non eseguire run_polling quando il file viene importato.
# Se vuoi testare in locale con python welcome_bot.py, puoi scommentare:
# if __name__ == "__main__":
#     get_application().run_polling()
