from aiogram import Router, F, types
from aiogram.filters import Command
from src.sql.db_api import DB


class INFORMATION:
    def __init__(self):
        self.router = Router()
        self.db = DB()
        
        self.router.message(Command("info"))(self.info)
        self.router.message(Command("eating"))(self.eating)
        self.router.message(Command("phone_numbers"))(self.phone_numbers)
        self.router.message(Command("events"))(self.events)

    async def info(self, message: types.Message):
        await message.answer(''' 
📞: (8152) 52 79 83 
📩: gymn6mail@yandex.ru 
🗺️: г. Мурманск, ул. Беринга д. 18, 183050 
''')

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

        text = '🎈 Мероприятия:\n\n'

        for event in data:
            text += f'🎈 {event.title}\n{event.text}\n\n*{event.time}*'

        await message.answer(text, parse_mode="Markdown")