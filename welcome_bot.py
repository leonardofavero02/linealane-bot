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
    "YouTube: <a href=\"https://www.youtube.com/@linealane\">YouTube</a>\n"
    "Facebook: <a href=\"https://www.facebook.com/DirettaLineaLane\">Diretta Linea Lane</a>\n\n"
    "🌍 Expat Lane:\n"
    "Vivi fuori dal Veneto? "
    "<a href=\"https://padlet.com/direttalinealane/expat-lane-acqlsf00zgd4grfg\">"
    "Iscriviti a Expat Lane e non sentirti più solo!</a>\n\n"
    "⚪🔴 Partecipa con rispetto.\n"
    "Ricorda che sei parte della nostra community!"
)


TACCAGNO_JOKES_MASTER = [
    "🧊💸 Controllate i frighi stanotte: se consumano troppo, a gennaio arriva solo il terzino in prestito… senza riscatto.",
    "❄️📉 Ho abbassato il termostato di mezzo grado: così risparmiamo abbastanza per un cartellino… forse.",
    "⚡🏃‍♂️ Se il frigo consuma come Nicola Rauti che corre dietro al pallone, qui non arriva luce fino a fine stagione.",
    "💡⏱️ Chi lascia le luci accese paga in minuti extra… così David Stückler farà più pressing… gratis.",
    "❄️🏔️ Allenamento al gelo: Carraro, Cavion e Zonta lo chiamano “preparazione in stile alpino”.",
    "📶🚫 Ho spento il Wi-Fi: se Filippo Alessio vuole segnare, che lo faccia col cuore, non con i meme.",
    "🚿❄️ Docce fredde! I ragazzi direbbero che è tattica di Gallo… ma è solo per risparmiare bollette.",
    "😬💡 Se cade la corrente, Leverbe e Cuomo dovranno illuminare il campo coi loro sorrisi.",
    "👟🧼 Ho promesso che chi spegne per ultimo il frigo avrà l’onore di lavare le scarpe di Pellizzari.",
    "🕯️⚽ Tattica a lume di candela con Claudio Morra: se segna, almeno usiamo la sua luminosità.",
    "🗣️🏃‍♂️📋 Chi parla troppo coi compagni paga con corsette extra… e Cester tiene il tabellino.",
    "🧊🏃‍♂️ Budget per riscaldamento = 0. Vitale e Tribuzzi? Si scaldano correndo… e basta.",
    "🔌🏟️ Se il Vicenza vuole un nuovo attaccante, prima spegniamo tutte le luci… anche quelle dello stadio.",
    "📊💸 Fabio Gallo ha detto sì alla corrente ridotta… ma solo dopo che Zamuner ha pagato la bolletta.",
    "😴🧊 Se Massolo resta sveglio stanotte, è solo per controllare se il frigo è ancora acceso.",
    "💡👔 Renzo Rosso è passato in sede e ha spento tutto: “Design minimal, budget rispettato”.",
    "📉💸 Stefano Rosso ha visto la bolletta e ha detto che così il terzino destro può aspettare febbraio.",
    "❄️🏃‍♂️ Cavion ha chiesto il riscaldamento: risposta del DS? “Scaldati correndo”.",
    "🔌😅 Renzo Rosso ha spento una luce e ha detto: “Ecco il bonus mercato”.",
    "🚿❄️ Docce fredde anche oggi: Stefano Rosso le chiama “sostenibilità applicata”.",
    "💡📋 Chi lascia una luce accesa fa allenamento extra con Cester che prende nota.",
    "⚡😬 Se salta la corrente, Leverbe e Cuomo tengono la linea… anche al buio.",
    "🧊👟 Frigo spento: Pellizzari ha capito che le scarpe si lavano solo a fine mese.",
    "🕯️⚽ Allenamento serale a lume di candela: Morra dice che così vede meglio la porta.",
    "📶🚫 Wi-Fi spento: Filippo Alessio protesta, il DS risponde “usa l’istinto”.",
    "❄️🏔️ Preparazione così dura che Vitale dice di essersi scaldato solo al novantesimo.",
    "💸🏟️ Stefano Rosso ha detto che se vogliamo un attaccante nuovo, prima spegniamo le luci dello stadio.",
    "🔌⚽ Renzo Rosso ha chiesto pressing alto… ma consumi bassissimi.",
    "🧊🏃‍♂️ Tribuzzi corre così tanto che il riscaldamento è diventato superfluo.",
    "💡😴 Massolo controlla il frigo come se fosse una porta da difendere.",
    "📊💸 Zamuner ha fatto i conti: una lampadina spenta vale mezzo cross in più.",
    "❄️⚽ Gallo parla di sacrificio, il termosifone resta spento per coerenza.",
    "🧊📉 Il DS ha abbassato il termostato: “Così respiriamo aria da playoff sostenibili”.",
    "🔦😬 Allenamento al buio: Carraro dice che migliora la visione di gioco.",
    "💡🏃‍♂️ Chi dimentica una luce accesa fa ripetute con Cavion fino a scaldarsi.",
    "❄️⚽ Zonta ha chiesto se arriva il riscaldamento: risposta “solo se segni”.",
    "📶❌ Internet spento in spogliatoio: Stefano Rosso dice che aumenta la concentrazione.",
    "🧊😅 Se il frigo resta acceso tutta la notte, Renzo Rosso manda il conto al mercato di gennaio.",
    "💡📋 Cester ha segnato sul tabellino: “Luce spenta, allenamento guadagnato”.",
    "❄️🏃‍♂️ Vitale dice che fa freddo, il DS risponde: “Corri più forte”.",
    "🔌⚽ Se cade la corrente, si gioca lo stesso: mentalità Lane.",
    "💸😬 Stefano Rosso ha sorriso vedendo la bolletta: “Ottimo, niente esterni nuovi”.",
    "🧊⚽ Morra a lume di candela dice che così sente meglio la porta.",
    "📉💡 Risparmio energetico così serio che anche il VAR è in modalità eco.",
    "❄️🏔️ Allenamento alpino approvato da Renzo Rosso: “È lifestyle”.",
    "🔦⚽ Luci spente in palestra: Gallo dice che è lavoro sulla percezione.",
    "💡🏃‍♂️ Se qualcuno accende una luce, Vitale parte in progressione per spegnerla.",
    "🧊📊 Il DS dice che il bilancio sta meglio… il frigo un po’ meno.",
    "❄️😴 Massolo dorme con una coperta in più: sacrificio per il mercato.",
    "🔌💸 Stefano Rosso ha detto che ogni watt risparmiato è un passo verso i playoff.",
    "🧊⚽ Se il Vicenza segna al novantesimo, è perché le luci erano spente prima.",
    "💡😅 Renzo Rosso passa in sede e spegne tutto: “Design pulito”.",
    "❄️🏃‍♂️ Chi si lamenta del freddo fa scatti con Tribuzzi fino a scaldarsi.",
    "📉⚽ Risparmio così serio che anche i palloni vengono gonfiati a metà.",
    "🔦😬 Allenamento serale: più ombre che luci, ma conti in ordine."
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

    message = get_next_luci_message()

    await context.bot.send_message(
        chat_id=GROUP_CHAT_ID,
        text=message,
        parse_mode="HTML"
    )

def get_next_luci_message():
    global luci_queue

    if not luci_queue:
        luci_queue = LUCI_MESSAGES_MASTER.copy()
        random.shuffle(luci_queue)

    return luci_queue.pop(0)


LUCI_MESSAGES_MASTER = [
    "💡⏰ <b>Sono le 23:00!</b>\nSpegnete le luci che consumano 🔌\nOgni watt risparmiato è un passo verso il mercato ⚽💸",

    "💡⏰ <b>23:00 precise.</b>\nLuci spente, sogni accesi ✨\nSe consumiamo meno, a gennaio arriva qualcuno 😏⚽",

    "💡⏰ <b>È scattata l’ora.</b>\nSpegnete tutto: luce, frigo, illusioni 💡🧊\nIl bilancio ringrazia 📊",

    "💡⏰ <b>23:00.</b>\nChiudere luci.\nRisparmiare energia.\nPensare al mercato.",

    "💡⏰ <b>Ore 23:00.</b>\nSacrificio anche fuori dal campo ❄️\nLuci spente = spirito Lane acceso 🔴⚪",

    "💡⏰ <b>23:00!</b>\nSpegnete le luci che costano più di un cartellino 😬\nGrazie per la collaborazione 💸⚽",

    "💡⏰ <b>23:00 – Comunicazione ufficiale</b>\nRidurre consumi immediatamente 🔌\nObiettivo: sostenibilità… e mercato 📉⚽",

    "💡⏰ <b>È ora.</b>\nLuce spenta oggi,\nesterno in più domani 😌⚽",

    "💡⏰ <b>23:00!</b>\nPiccoli gesti, grande Lane 🔴⚪\nSpegni la luce, accendi il futuro ⚽✨",

    "💡⏰ <b>23:00.</b>\nSpegnete le luci.\nIl mercato vi guarda 👀💸⚽"
]

luci_queue = []


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
