from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message,
    CallbackQuery,
)

from bot import app
from bot.config import config
from bot.database.mongodb import add_served_chat, add_served_user

START_TEXT = """
✨ **Namaste {mention}!**

Main hu **{bot_name}** — tumhara personal music companion jo group voice chats mein high-quality music stream karta hu 🎶

╭─────────────────────╮
   🎧 **Kya kya kar sakta hu:**
╰─────────────────────╯
▸ 🎵 YouTube se koi bhi gaana play karna
▸ 📃 Poori playlist queue karna
▸ ⏯ Pause / Resume / Skip / End
▸ 🔁 Loop mode
▸ 👑 Admin-only controls
▸ ⚡ Super fast & lag-free streaming

**Mujhe apne group mein add karo aur `/play <song name>` bhejo!**
"""

HELP_TEXT = """
📖 **Command List**

**➻ /play** `<song name / link>` — gaana play karo
**➻ /pause** — music pause karo
**➻ /resume** — music resume karo
**➻ /skip** — agla gaana
**➻ /end** — voice chat se music band karo
**➻ /queue** — queue dekho
**➻ /loop** — loop mode on/off
**➻ /ping** — bot ka response time
**➻ /stats** — bot statistics

👑 = sirf group admins use kar sakte hain
"""


def start_buttons():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("➕ Add me to your group", url=f"https://t.me/{app.me.username}?startgroup=true")
            ],
            [
                InlineKeyboardButton("📖 Commands", callback_data="help_menu"),
                InlineKeyboardButton("👨‍💻 Support", url=f"https://t.me/{config.SUPPORT_GROUP}") if config.SUPPORT_GROUP else InlineKeyboardButton("👨‍💻 Support", url="https://t.me/telegram"),
            ],
            [
                InlineKeyboardButton("📢 Updates", url=f"https://t.me/{config.SUPPORT_CHANNEL}") if config.SUPPORT_CHANNEL else InlineKeyboardButton("🌐 GitHub", url="https://github.com"),
            ],
        ]
    )


def back_button():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔙 Back", callback_data="back_start")]]
    )


@app.on_message(filters.command("start"))
async def start_cmd(client, message: Message):
    await add_served_user(message.from_user.id)
    if message.chat.type != "private":
        await add_served_chat(message.chat.id)

    text = START_TEXT.format(
        mention=message.from_user.mention,
        bot_name=config.BOT_NAME,
    )
    await message.reply_photo(
        photo=config.START_IMG,
        caption=text,
        reply_markup=start_buttons(),
    )


@app.on_callback_query(filters.regex("help_menu"))
async def help_menu(client, cb: CallbackQuery):
    await cb.message.edit_caption(HELP_TEXT, reply_markup=back_button())


@app.on_callback_query(filters.regex("back_start"))
async def back_start(client, cb: CallbackQuery):
    text = START_TEXT.format(
        mention=cb.from_user.mention,
        bot_name=config.BOT_NAME,
    )
    await cb.message.edit_caption(text, reply_markup=start_buttons())
