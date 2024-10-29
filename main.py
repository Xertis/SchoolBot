import asyncio
from config import *
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import os
import psutil
from aiogram import Bot, Dispatcher, types
from src.sql import AsyncSQL
from src.routers.info_router import info_router
from src.routers.classes_router import classes_router
from src.utils.no_command_callback import no_command

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    dp.include_routers(no_command, info_router, classes_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

