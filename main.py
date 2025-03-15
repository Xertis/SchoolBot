import asyncio
import logging
from src.utils.env import Constants
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from src.sql.db_api import DB

from src.keyboards.reply_keyboard import BuildReplyButtons

from src.routers.info_router import INFORMATION
from src.routers.root_router import ROOT

from src.utils.no_command_callback import no_command


logging.basicConfig(level=logging.INFO)
bot = Bot(token=Constants.TOKEN)
dp = Dispatcher()
db = DB()

inforation = INFORMATION()
root = ROOT()


async def main():
    dp.include_routers(inforation.router, no_command, root.router)
    await dp.start_polling(bot)


@dp.message(Command("start"))
async def start(message: types.Message):

    help = [
        [['Информация', inforation.info, False]],
        [['Питание', inforation.eating, False]],
        [['Мероприятия', inforation.events, False]],
        [['Контакты', inforation.phone_numbers, False]]
    ]

    if db.admins.has(message.from_user.id):
        help.append([['Редактировать [ADMIN]', root.help, False]])

    await message.answer("зелебоба", parse_mode="Markdown", reply_markup=await BuildReplyButtons(help))

if __name__ == "__main__":
    asyncio.run(main())
