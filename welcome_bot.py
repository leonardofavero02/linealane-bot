import os
import random
from datetime import time
import pytz

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    filters,
    ContextTypes
)

# =====================
# CONFIG
# =====================

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN env var not set")

TIMEZONE = pytz.timezone("Europe/Rome")

GROUP_CHAT_ID = None
ADMIN_IDS = set()  # verranno popolati automaticamente

WELCOME_MESSAGE = (
    "‼️💬 Benvenuto/a {first_name} nel gruppo Linea Lane!\n\n"
    "📘 Codice di Condotta:\n"
    "<a href=\"https://telegra.ph/Reg-Community-08-29\">Regole della Community</a>\n\n"
    "🌐 Social:\n"
    "Instagram: <a href=\"https://www.instagram.com/linea_lane/\">Instagram</a>\n"
    "YouTube: <a href=\"https://www.youtube.com/@linealane\">YouTube</a>\n\n"
    "⚪🔴 Partecipa con rispetto.\n"
    "Ricorda che sei parte della nostra community!"
)

TACCAGNO_JOKES_MASTER = [
    "🧊💸 Controllate i frighi stanotte: se consumano troppo, a gennaio arriva solo il terzino in prestito… senza riscatto.",
    "❄️📉 Ho abbassato il termostato di mezzo grado: così risparmiamo abbastanza per un cartellino… forse.",
    "⚡🏃‍♂️ Se il frigo consuma come Nicola Rauti che corre dietro al pallone, qui non arriva luce fino a fine stagione.",
    "💡⏱️ Chi lascia le luci accese paga in minuti extra… così David Stückler farà più pressing… gratis.",
    "❄️🏔️ Allenamento al gelo: Carraro, Cavion e Zonta lo chiamano ‘preparazione in stile alpino’.",
    "📶🚫 Ho spento il Wi-Fi: se Filippo Alessio vuole segnare, che lo faccia col cuore, non con i meme.",
    "🚿❄️ Docce fredde! I ragazzi direbbero che è tattica di Gallo… ma è solo per risparmiare bollette.",
    "😬💡 Se cade la corrente, Leverbe e Cuomo dovranno illuminare il campo coi loro sorrisi.",
    "👟🧼 Ho promesso che chi spegne per ultimo il frigo avrà l’onore di lavare le scarpe di Pellizzari.",
    "🕯️⚽ Tattica a lume di candela con Claudio Morra: se segna, almeno usiamo la sua luminosità.",
    "🗣️🏃‍♂️📋 Chi parla troppo coi compagni paga con corsette extra… e Cester tiene il tabellino.",
    "🧊🏃‍♂️ Budget per riscaldamento = 0. Vitale e Tribuzzi? Si scaldano correndo… e basta.",
    "🔌🏟️ Se il Vicenza vuole un nuovo attaccante, prima spegniamo tutte le luci… anche quelle dello stadio.",
    "📊💸 Fabio Gallo ha detto sì alla corrente ridotta… ma solo dopo che Zamuner ha pagato la bolletta.",
    "😴🧊 Se Massolo resta sveglio stanotte, è solo per controllare se il frigo è ancora acceso."
]

# Copia di lavoro (rotazione senza ripetizioni)
taccagno_queue = []

# =====================
# HELPERS
# =====================

def get_next_joke():
    global taccagno_queue

    if not taccagno_queue:
        taccagno_queue = TACCAGNO_JOKES_MASTER.copy()
        random.shuffle(taccagno_queue)

    return taccagno_queue.pop(0)

# =====================
# HANDLERS
# =====================

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

async def capture_chat_and_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global GROUP_CHAT_ID

    GROUP_CHAT_ID = update.effective_chat.id

    if update.effective_user:
        ADMIN_IDS.add(update.effective_user.id)

async def luci_off(context: ContextTypes.DEFAULT_TYPE):
    if GROUP_CHAT_ID is None:
        return

    await context.bot.send_message(
        chat_id=GROUP_CHAT_ID,
        text=(
            "💡⏰ **Sono le 23:00!**\n"
            "Spegnete le luci che consumano!\n\n"
            "💸⚽ Altrimenti l’esterno e il difensore a gennaio **non arrivano** 😤"
        ),
        parse_mode="HTML"
    )

async def taccagno_daily(context: ContextTypes.DEFAULT_TYPE):
    if GROUP_CHAT_ID is None:
        return

    joke = get_next_joke()
    await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=joke)

async def taccagno_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return

    joke = get_next_joke()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=joke)

# =====================
# APP FACTORY
# =====================

def get_application():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    app.add_handler(MessageHandler(filters.ALL, capture_chat_and_admin), group=1)
    app.add_handler(CommandHandler("taccagno", taccagno_command))

    # Messaggio fisso 23:00
    app.job_queue.run_daily(
        luci_off,
        time=time(hour=23, minute=0, tzinfo=TIMEZONE)
    )

    # Battuta random giornaliera
    hour = random.randint(10, 21)
    minute = random.randint(0, 59)

    app.job_queue.run_daily(
        taccagno_daily,
        time=time(hour=hour, minute=minute, tzinfo=TIMEZONE)
    )

    return app
