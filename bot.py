import asyncio
from aiogram import Dispatcher, Bot
import logging

from database.db_client import db
from handlers import start_handler, task_handler
from config import env


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    bot = Bot(env("BOT_TOKEN"))
    dp = Dispatcher()
    dp.include_routers(start_handler.router,
                       task_handler.router,
                       )
    await db.create_user_table()
    await db.create_tasks_table()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
