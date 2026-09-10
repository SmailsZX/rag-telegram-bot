import asyncio

from app.bot import start_bot


if __name__ == "__main__":
    try:
        asyncio.run(start_bot())
    except (KeyboardInterrupt, SystemExit):
        print("\n👋 Бот остановлен.")