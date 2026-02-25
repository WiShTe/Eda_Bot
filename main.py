from __future__ import annotations # just type hints handling

import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from handlers import all_routers

from database.database import database

BOT_TOKEN_ENV = "BOT_TOKEN"





async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    load_dotenv()

    token = os.getenv(BOT_TOKEN_ENV)
    if not token:
        raise RuntimeError(
            f"Set the {BOT_TOKEN_ENV} environment variable with your bot token."
        )

    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    # подключение всех роутеров (start_router,)
    for router in all_routers:
        dp.include_router(router)
    await database.create_pool()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())