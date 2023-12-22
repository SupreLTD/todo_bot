import asyncio
from aiogram import Dispatcher, Bot
import logging

from handlers import start_handler
from config import env
from db_client import Database

db = Database()


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    bot = Bot(env("BOT_TOKEN"))
    dp = Dispatcher()
    dp.include_router(start_handler.router)
    await db.create_user_table()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())