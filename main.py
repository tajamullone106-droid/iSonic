import asyncio
import importlib
import os

from bot import app, assistant, call_py
from bot.config import config

# Auto-import every module inside bot/modules so handlers get registered
MODULES_DIR = os.path.join(os.path.dirname(__file__), "bot", "modules")
for filename in os.listdir(MODULES_DIR):
    if filename.endswith(".py") and filename != "__init__.py":
        importlib.import_module(f"bot.modules.{filename[:-3]}")


async def main():
    print("🎵 Starting bot client...")
    await app.start()

    print("👤 Starting assistant client...")
    await assistant.start()

    print("📞 Starting PyTgCalls...")
    await call_py.start()

    me = await app.get_me()
    print(f"✅ {me.first_name} is up and running!")

    await asyncio.Event().wait()  # keep running forever


if __name__ == "__main__":
    asyncio.run(main())
