from pyrogram import filters
from pyrogram.types import Message
from pytgcalls.types import MediaStream
from pytgcalls.exceptions import NoActiveGroupCall

from bot import app, call_py
from bot.utils.downloader import search_track, download_audio
from bot.database.mongodb import add_to_queue, get_queue, pop_queue, clear_queue


async def _play_next(chat_id: int):
    """Pop next track from queue and stream it. Called after a track ends."""
    queue = await get_queue(chat_id)
    if not queue:
        await call_py.leave_call(chat_id)
        return

    track = queue[0]
    await call_py.play(chat_id, MediaStream(track["file_path"]))


@app.on_message(filters.command("play") & filters.group)
async def play_cmd(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            "⚠️ **Usage:** `/play <song name or YouTube link>`"
        )

    query = message.text.split(None, 1)[1]
    status = await message.reply_text(f"🔎 **Searching:** `{query}` ...")

    info = await search_track(query)
    if not info:
        return await status.edit_text("❌ Koi result nahi mila, dusra naam try karo.")

    await status.edit_text(f"⬇️ **Downloading:** {info['title']}")
    file_path = download_audio(info["link"])
    info["file_path"] = file_path

    chat_id = message.chat.id
    queue = await get_queue(chat_id)
    await add_to_queue(chat_id, info)

    if len(queue) == 0:
        # Nothing was playing — start immediately
        try:
            await call_py.play(chat_id, MediaStream(file_path))
        except NoActiveGroupCall:
            return await status.edit_text(
                "❌ **Voice chat active nahi hai!**\nPehle group me VC start karo."
            )
        await status.edit_text(
            f"▶️ **Now Playing:**\n🎵 {info['title']}\n"
            f"⏱ {info['duration']} | 🎤 {info['channel']}\n\n"
            f"Requested by: {message.from_user.mention}"
        )
    else:
        await status.edit_text(
            f"✅ **Added to queue (#{len(queue)}):**\n🎵 {info['title']}"
        )


@app.on_message(filters.command("queue") & filters.group)
async def queue_cmd(client, message: Message):
    queue = await get_queue(message.chat.id)
    if not queue:
        return await message.reply_text("📭 **Queue khali hai.**")

    text = "📃 **Current Queue:**\n\n"
    for i, track in enumerate(queue, start=1):
        marker = "▶️ Now Playing" if i == 1 else f"{i}."
        text += f"{marker} — {track['title']}\n"

    await message.reply_text(text)


@call_py.on_stream_end()
async def on_stream_end(client, update):
    chat_id = update.chat_id
    await pop_queue(chat_id)
    await _play_next(chat_id)
