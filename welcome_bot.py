import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters
)

# =====================================================
# CONFIGURAZIONE
# =====================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN env var not set")

# =====================================================
# MESSAGGIO DI BENVENUTO
# =====================================================

WELCOME_MESSAGE = (
    "‼️💬 Benvenuto/a {first_name} nel gruppo Linea Lane!\n\n"
    "📘 Codice di Condotta:\n"
    "<a href=\"https://telegra.ph/Reg-Community-08-29\">Regole della Community</a>\n\n"
    "🌐 Social:\n"
    "Instagram: <a href=\"https://www.instagram.com/linea_lane/\">Instagram</a>\n"
    "YouTube: <a href=\"https://www.youtube.com/@linealane\">YouTube</a>\n"
    "Facebook: <a href=\"https://www.facebook.com/DirettaLineaLane\">Diretta Linea Lane</a>\n\n"
    "🌍 Expat Lane:\n"
    "Vivi fuori dal Veneto?\n"
    "<a href=\"https://padlet.com/direttalinealane/expat-lane-acqlsf00zgd4grfg\">"
    "Iscriviti a Expat Lane</a>\n\n"
    "⚪🔴 Partecipa con rispetto.\n"
    "Sei parte della nostra community!"
)

# =====================================================
# HANDLER BENVENUTO
# =====================================================

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.new_chat_members:
        for member in update.message.new_chat_members:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=WELCOME_MESSAGE.format(
                    first_name=member.first_name or "amico/a"
                ),
                parse_mode="HTML",
                disable_web_page_preview=True
            )

# =====================================================
# APP FACTORY
# =====================================================

def get_application():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(
        MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome)
    )

    return app
