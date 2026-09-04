from pyrogram import Client
from pytgcalls import PyTgCalls

from bot.config import config

# Main bot client (runs as a bot account)
app = Client(
    "MusicBot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
)

# Assistant client (userbot, needed to actually join & stream in voice chats)
assistant = Client(
    "MusicAssistant",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    session_string=config.SESSION_STRING,
)

# PyTgCalls instance bound to the assistant
call_py = PyTgCalls(assistant)
