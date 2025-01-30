from aiogram import Router, F, types
from aiogram.filters import Command
from src.sql.db_api import DB
from constants import NEW_LINE_SYMBOL
from src.utils.loader import LOADER


class INFORMATION:
    def __init__(self):
        self.router = Router()
        self.db = DB()
        
        self.router.message(Command("info"))(self.info)
        self.router.message(Command("eating"))(self.eating)
        self.router.message(Command("phone_numbers"))(self.phone_numbers)
        self.router.message(Command("events"))(self.events)

    @staticmethod
    async def __parse__(heading, data, message: types.Message):
        text = ''
        if_for_run = False

        await message.answer(heading, parse_mode="Markdown")

        for block in data:
            if_for_run = True
            new_line = f"*{block.title}*\n\n{block.text}\n\n*{block.time}*\n"

            if hasattr(block, "image_id"):
                await message.answer_photo(photo=types.FSInputFile(path=LOADER.get_image_path(block.image_id)), caption=new_line, parse_mode="Markdown")
            else:
                text += NEW_LINE_SYMBOL + new_line

        if not if_for_run:
            text += "😕 Не найдено"
        else:
            return

        await message.answer(text, parse_mode="Markdown")

    async def info(self, message: types.Message):
        message_text = '''
            🏫 Основная информация о гимназии:

            📞: (8152) 52 79 83
            📩: gymn6mail@yandex.ru
            🗺️: г. Мурманск, ул. Беринга д. 18, 183050
        '''

        message_text = '\n'.join(line.strip() for line in message_text.splitlines())
        await message.answer(message_text)


    async def eating(self, message: types.Message):
        await message.answer('W.I.P.')

    async def phone_numbers(self, message: types.Message):
        numbers = self.db.numbers.get_all()

        text = '☎️ Контакты:\n\n'

        for number in numbers:
            text += f'📞 {number.owner}: {number.number}\n'

        await message.answer(text)

    async def events(self, message: types.Message):
        data = self.db.events.get_all()

        await self.__parse__("🎈 Мероприятия:", data, message)