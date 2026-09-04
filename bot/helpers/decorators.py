from functools import wraps
from pyrogram import types
from pyrogram.enums import ChatMemberStatus
from bot.config import config


def admin_only(func):
    """Only group admins (or the bot owner) can use this command."""

    @wraps(func)
    async def wrapper(client, message: types.Message, *args, **kwargs):
        if message.chat.type == "private":
            return await func(client, message, *args, **kwargs)

        if message.from_user and message.from_user.id == config.OWNER_ID:
            return await func(client, message, *args, **kwargs)

        member = await message.chat.get_member(message.from_user.id)
        if member.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER,
        ):
            return await func(client, message, *args, **kwargs)

        return await message.reply_text(
            "🚫 **Sirf group admins is command ko use kar sakte hain!**"
        )

    return wrapper
