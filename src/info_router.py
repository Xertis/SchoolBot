from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile, InputFile
from src.sql import AsyncSQL
from src.keyboards.reply_keyboard import BuildReplyButtons
from src.utils.no_command_callback import AddToNoCommand
from src.

info_router = Router()
db = AsyncSQL('database.db')

@info_router.message(Command("info"))
async def info(message: types.Message):
    await message.answer('''
📞: (8152) 52 79 83
📩: gymn6mail@yandex.ru
🗺️: г .Мурманск, ул. Беринга д. 18, 183050
''')
    
@info_router.message(Command("eating"))
async def eating(message: types.Message):
    pass

@info_router.message(Command("start"))
async def start(message: types.Message):

    help = [
        [['Информация', info]],
        [['О классах', classes], ['Питание', eating]],
        [['Отзыв и контакты', classes]]
    ]

    await message.answer("зелебоба", parse_mode="Markdown", reply_markup = BuildReplyButtons(help))