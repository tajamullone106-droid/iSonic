from pyrogram import filters
from pyrogram.types import Message
from pytgcalls.types import MediaStream

from bot import app, call_py
from bot.helpers.decorators import admin_only
from bot.database.mongodb import (
    get_queue,
    pop_queue,
    clear_queue,
    get_settings,
    set_loop,
)


@app.on_message(filters.command("pause") & filters.group)
@admin_only
async def pause_cmd(client, message: Message):
    await call_py.pause(message.chat.id)
    await message.reply_text("⏸ **Music paused.**")


@app.on_message(filters.command("resume") & filters.group)
@admin_only
async def resume_cmd(client, message: Message):
    await call_py.resume(message.chat.id)
    await message.reply_text("▶️ **Music resumed.**")


@app.on_message(filters.command("skip") & filters.group)
@admin_only
async def skip_cmd(client, message: Message):
    chat_id = message.chat.id
    await pop_queue(chat_id)
    queue = await get_queue(chat_id)

    if not queue:
        await call_py.leave_call(chat_id)
        return await message.reply_text("⏹ **Queue khatam — voice chat se nikal gaya.**")

    next_track = queue[0]
    await call_py.play(chat_id, MediaStream(next_track["file_path"]))
    await message.reply_text(f"⏭ **Skipped!** Now playing: {next_track['title']}")


@app.on_message(filters.command("end") & filters.group)
@admin_only
async def end_cmd(client, message: Message):
    chat_id = message.chat.id
    await call_py.leave_call(chat_id)
    await clear_queue(chat_id)
    await message.reply_text("⏹ **Stream ended aur queue clear kar di.**")


@app.on_message(filters.command("loop") & filters.group)
@admin_only
async def loop_cmd(client, message: Message):
    settings = await get_settings(message.chat.id)
    new_value = not settings.get("loop", False)
    await set_loop(message.chat.id, new_value)
    status = "ON 🔁" if new_value else "OFF"
    await message.reply_text(f"**Loop mode:** {status}")
