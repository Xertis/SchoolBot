from aiogram import Router, F, types, Bot
from aiogram.filters import Command
from src.sql.db_api import DB
from src.utils.loader import LOADER


class ROOT:
    def __init__(self):
        self.router = Router()
        self.db = DB()
        
        self.router.message(F.document)(self.create_event)
        
    async def create_event(self, message: types.Message, bot: Bot):
        doc = message.document
        file_id = message.document.file_id

        file = await bot.get_file(file_id)
        file_path = file.file_path

        index = LOADER.get_new_index()

        new_path = f"{LOADER.get_path() + str(index)}.jpg"
        await bot.download_file(file_path=file_path, destination=new_path)

        self.db.images.add(index)