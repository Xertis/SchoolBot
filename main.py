import asyncio
import logging
import schedule
from src.utils.env import Constants
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from src.tasks.tasks import EventsCleaner, MealCleaner
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

async def reg_scheduler_tasks():
    schedule.every(1).minutes.do(EventsCleaner)
    schedule.every(1).days.do(MealCleaner)

async def main():
    await reg_scheduler_tasks()
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler())

    dp.include_routers(inforation.router, no_command, root.router)
    await dp.start_polling(bot)

async def scheduler():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

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

    await message.answer("Бот запущен", parse_mode="Markdown", reply_markup=await BuildReplyButtons(help))

if __name__ == "__main__":
    asyncio.run(main())
