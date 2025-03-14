from aiogram import Router, F, types, Bot
from aiogram.filters import Command
from src.sql.db_api import DB
from src.utils.loader import LOADER
from src.utils.parsers import Parsers
from src.keyboards.inline_keyboard import BuildInlineButtons
from aiogram.fsm.context import FSMContext
from src.state_machines.states import WaitDocument
from aiogram.utils.markdown import hbold, hunderline
from datetime import datetime
import os


class ROOT:
    def __init__(self):
        self.router = Router()
        self.db = DB()

        self.router.message(Command("root_help"))(self.help)
        self.router.callback_query(F.data == "root.help")(self.edit_eating_start)
        self.router.message(WaitDocument.Wait, F.document)(self.edit_eating_finish)

    async def edit_eating_start(self, callback_query: types.CallbackQuery, state: FSMContext):
        await state.set_state(WaitDocument.Wait)
        await callback_query.message.answer("Отправьте *.csv* таблицу с новым питанием", parse_mode="Markdown")
        await callback_query.answer()

    async def edit_eating_finish(self, message: types.Message, state: FSMContext, bot: Bot):
        document = message.document
        file = await bot.get_file(document.file_id)
        file_path = file.file_path

        await bot.download_file(file_path=file_path, destination=LOADER.get_eating())
        eating_data = Parsers.eating.parse(LOADER.get_eating())

        time_edit = os.path.getmtime(LOADER.get_eating())
        date = datetime.fromtimestamp(time_edit).strftime("%d.%m.%Y")
        
        eating_message = Parsers.eating.to_str(eating_data, date)

        await message.answer(eating_message, parse_mode="HTML")

        await message.answer(f"Питание обновлено.")
        await state.clear()
    
        
    async def create_event(self, message: types.Message, bot: Bot):
        file_id = message.document.file_id

        file = await bot.get_file(file_id)
        file_path = file.file_path

        index = LOADER.get_new_index()

        new_path = f"{LOADER.get_path() + str(index)}.jpg"
        await bot.download_file(file_path=file_path, destination=new_path)

        self.db.images.add(index)

    async def help(self, message: types.Message):
        if not self.db.admins.has(message.from_user.id):
            return
        
        help = [
            [['Изменить питание', "root.help"]],
        ]
        
        await message.answer("Выберите действие:", parse_mode="Markdown", reply_markup = await BuildInlineButtons(help))