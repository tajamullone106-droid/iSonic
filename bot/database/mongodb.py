from motor.motor_asyncio import AsyncIOMotorClient
from bot.config import config

_client = AsyncIOMotorClient(config.MONGO_URI)
db = _client["musicbot"]

queues_col = db["queues"]          # per-chat song queue
settings_col = db["settings"]      # per-chat settings (loop, volume..)
served_chats_col = db["served_chats"]
served_users_col = db["served_users"]


# ---------- QUEUE HELPERS ----------

async def get_queue(chat_id: int) -> list:
    doc = await queues_col.find_one({"chat_id": chat_id})
    return doc["queue"] if doc else []


async def add_to_queue(chat_id: int, track: dict):
    doc = await queues_col.find_one({"chat_id": chat_id})
    if doc:
        await queues_col.update_one(
            {"chat_id": chat_id}, {"$push": {"queue": track}}
        )
    else:
        await queues_col.insert_one({"chat_id": chat_id, "queue": [track]})


async def pop_queue(chat_id: int):
    """Remove and return the currently playing (first) track."""
    doc = await queues_col.find_one({"chat_id": chat_id})
    if not doc or not doc["queue"]:
        return None
    first = doc["queue"][0]
    await queues_col.update_one({"chat_id": chat_id}, {"$pop": {"queue": -1}})
    return first


async def clear_queue(chat_id: int):
    await queues_col.delete_one({"chat_id": chat_id})


# ---------- SETTINGS HELPERS ----------

async def get_settings(chat_id: int) -> dict:
    doc = await settings_col.find_one({"chat_id": chat_id})
    if not doc:
        default = {"chat_id": chat_id, "loop": False, "volume": 100}
        await settings_col.insert_one(default)
        return default
    return doc


async def set_loop(chat_id: int, value: bool):
    await settings_col.update_one(
        {"chat_id": chat_id}, {"$set": {"loop": value}}, upsert=True
    )


# ---------- STATS HELPERS ----------

async def add_served_chat(chat_id: int):
    if not await served_chats_col.find_one({"chat_id": chat_id}):
        await served_chats_col.insert_one({"chat_id": chat_id})


async def add_served_user(user_id: int):
    if not await served_users_col.find_one({"user_id": user_id}):
        await served_users_col.insert_one({"user_id": user_id})


async def get_served_chats_count() -> int:
    return await served_chats_col.count_documents({})


async def get_served_users_count() -> int:
    return await served_users_col.count_documents({})
