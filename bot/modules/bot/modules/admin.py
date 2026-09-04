import time
import psutil
from pyrogram import filters
from pyrogram.types import Message

from bot import app
from bot.config import config
from bot.database.mongodb import get_served_chats_count, get_served_users_count


@app.on_message(filters.command("ping"))
async def ping_cmd(client, message: Message):
    start = time.time()
    msg = await message.reply_text("🏓 Pinging...")
    ping_ms = (time.time() - start) * 1000
    await msg.edit_text(f"🏓 **Pong!** `{ping_ms:.2f} ms`")


@app.on_message(filters.command("stats"))
async def stats_cmd(client, message: Message):
    chats = await get_served_chats_count()
    users = await get_served_users_count()
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent

    text = (
        "📊 **Bot Statistics**\n\n"
        f"👥 **Chats:** {chats}\n"
        f"🙋 **Users:** {users}\n"
        f"🖥 **CPU Usage:** {cpu}%\n"
        f"💾 **RAM Usage:** {ram}%\n"
    )
    await message.reply_text(text)


@app.on_message(filters.command("broadcast") & filters.user(config.OWNER_ID))
async def broadcast_cmd(client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("⚠️ Kisi message ko reply karke `/broadcast` bhejo.")

    from bot.database.mongodb import served_chats_col

    sent, failed = 0, 0
    async for chat in served_chats_col.find():
        try:
            await message.reply_to_message.copy(chat["chat_id"])
            sent += 1
        except Exception:
            failed += 1

    await message.reply_text(f"✅ Broadcast done!\nSent: {sent} | Failed: {failed}")
