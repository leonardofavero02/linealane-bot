import os
import sqlite3

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

DB_FILE = "identities.db"

# =====================================================
# DATABASE
# =====================================================

def init_db():
    conn = sqlite3.connect(DB_FILE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS identities (
            user_id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            username TEXT
        )
    """)

    conn.commit()
    conn.close()


def get_user(user_id):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row

    row = conn.execute(
        """
        SELECT *
        FROM identities
        WHERE user_id = ?
        """,
        (user_id,)
    ).fetchone()

    conn.close()

    return row


def save_user(
    user_id,
    first_name,
    last_name,
    username
):
    conn = sqlite3.connect(DB_FILE)

    conn.execute(
        """
        INSERT OR REPLACE INTO identities
        (
            user_id,
            first_name,
            last_name,
            username
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            first_name,
            last_name,
            username
        )
    )

    conn.commit()
    conn.close()


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
# BENVENUTO NUOVI MEMBRI
# =====================================================

async def welcome(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
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
# RILEVAZIONE CAMBIO NOME
# =====================================================

async def track_name_change(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if not update.message:
        return

    user = update.effective_user

    if not user:
        return

    if user.is_bot:
        return

    current_first = user.first_name or ""
    current_last = user.last_name or ""
    current_username = user.username or ""

    old = get_user(user.id)

    # Prima volta: registra senza notificare
    if old is None:

        save_user(
            user.id,
            current_first,
            current_last,
            current_username
        )

        return

    changed = (
        old["first_name"] != current_first
        or old["last_name"] != current_last
        or old["username"] != current_username
    )

    if not changed:
        return

    old_name = (
        f'{old["first_name"] or ""} '
        f'{old["last_name"] or ""}'
    ).strip()

    new_name = (
        f'{current_first} '
        f'{current_last}'
    ).strip()

    old_username = old["username"] or "-"
    new_username = current_username or "-"

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            "🔄 <b>Cambio nome rilevato</b>\n\n"
            f"<b>Prima:</b> {old_name}\n"
            f"<b>Ora:</b> {new_name}\n\n"
            f"<b>Username:</b>\n"
            f"@{old_username} → @{new_username}"
        ),
        parse_mode="HTML"
    )

    save_user(
        user.id,
        current_first,
        current_last,
        current_username
    )

# =====================================================
# APP FACTORY
# =====================================================

def get_application():

    init_db()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.StatusUpdate.NEW_CHAT_MEMBERS,
            welcome
        )
    )

    app.add_handler(
        MessageHandler(
            filters.ALL,
            track_name_change
        )
    )

    return app
