from aiogram import Router, F, types
from aiogram.filters import Command
from src.sql.db_api import DB
from src.utils.env import Constants
from src.utils.loader import LOADER
from src.utils.parsers import Parsers
from src.utils.calendar import get_calendar_keyboard, get_main_calendar_keyboard
from datetime import datetime
from src.keyboards.inline_keyboard import BuildInlineButtons
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hbold, hunderline

async def ShowEvents(heading: str, data: list, keyboard: types.InlineKeyboardMarkup=None, message: types.Message=None):
    text = ''
    if_for_run = False

    await message.answer(heading, parse_mode="Markdown")

    for block in data:
        if_for_run = True
        time = block.time.strftime(Constants.DATE_FORMAT)
        new_line = f"🎈: *{block.title}*\n\n{block.text}\n\n⏰: _{time}_\n"

        if hasattr(block, "image_id"):
            await message.answer_photo(photo=types.FSInputFile(path=LOADER.get_image_path(block.image_id)), 
                caption=new_line, 
                parse_mode="Markdown",
                reply_markup=keyboard
            )
        else:
            text += Constants.NEW_LINE_SYMBOL + new_line

    if not if_for_run:
        text += "😕 Мероприятия не найдены"
    else:
        return

    await message.edit_text(text, parse_mode="Markdown", reply_markup=keyboard)


class INFORMATION:
    def __init__(self):
        self.router = Router()
        self.db = DB()

        self.router.message(Command("info"))(self.info)
        self.router.message(Command("eating"))(self.eating)
        self.router.message(Command("phone_numbers"))(self.phone_numbers)
        self.router.message(Command("events"))(self.events)
        self.router.callback_query(F.data == "info.events.lenta")(self.events_lenta)
        self.router.callback_query(self.calendar_checker)(self.events_calendar)

    @staticmethod
    async def calendar_checker(callback):
        calendar_events = ("open_calendar", "select_date:", "date_change:", "back_to_main")
        for event in calendar_events:
            if callback.data.startswith(event):
                return True
        return False

    async def info(self, message: types.Message):
        message_text = '''
            🏫 Основная информация о гимназии:

            📞: (8152) 52 79 83
            📩: gymn6mail@yandex.ru
            🗺️: г. Мурманск, ул. Беринга д. 18, 183050
        '''

        message_text = '\n'.join(line.strip()
                                 for line in message_text.splitlines())
        await message.answer(message_text)

    async def eating(self, message: types.Message):
        eating_data = Parsers.eating.parse_from_db(self.db.meal.get_all())
        eating_message = Parsers.eating.to_str(eating_data)
        await message.answer(eating_message, parse_mode="HTML")\
        
    async def events(self, message: types.Message):
        current_date = datetime.today().date()
        date_text = current_date.strftime("%Y-%m-%d")

        help = [
            [['Открыть ленту мероприятий', "info.events.lenta"]],
            [['Открыть календарь мероприятий', "date_change:" + date_text]],
        ]

        await message.answer("Выберите действие:", parse_mode="Markdown", reply_markup=await BuildInlineButtons(help))

    async def events_lenta(self, callback_query: types.CallbackQuery):
        data = self.db.events.get_all()
        await ShowEvents(heading="🎈 Мероприятия:", data=data, message=callback_query.message)
        await callback_query.answer()

    async def events_calendar(self, callback_query: types.CallbackQuery, state: FSMContext):
        data = callback_query.data
        current_date = await state.get_data() or {"current_date": datetime.today().date()}
        current_date = current_date["current_date"]
        
        if data.startswith("date_change:"):
            new_date = datetime.strptime(data.split(":")[1], "%Y-%m-%d").date()
            await state.update_data(current_date=new_date)
            await self.events_print(callback_query=callback_query, current_date=new_date)
            await callback_query.message.edit_reply_markup(reply_markup=await get_main_calendar_keyboard(new_date))
        
        elif data == "open_calendar":
            await callback_query.message.edit_reply_markup(reply_markup=await get_calendar_keyboard(current_date))
        
        elif data.startswith("select_date:"):
            selected_date = datetime.strptime(data.split(":")[1], "%Y-%m-%d").date()
            await state.update_data(current_date=selected_date)
            await self.events_print(callback_query=callback_query, current_date=selected_date)
            await callback_query.message.edit_reply_markup(reply_markup=await get_main_calendar_keyboard(selected_date))
        
        elif data == "back_to_main":
            await callback_query.message.edit_reply_markup(reply_markup=await get_main_calendar_keyboard(current_date))
        
        await callback_query.answer()

    async def events_print(self, callback_query: types.CallbackQuery, current_date: datetime):
        data = self.db.events.get_by_date(current_date)
        new_text = "🎈 Мероприятия:\n"

        for i, event in enumerate(data):
            new_text += hbold(f"{i+1}. {event.title}\n\n")
            new_text += f"{event.text}\n\n"
            new_text += hunderline(event.time.time().strftime(Constants.TIME_FORMAT))
            new_text += "\n - - - - -\n"

        if new_text == "🎈 Мероприятия:\n":
            new_text += "😕 Мероприятия не найдены"

        await callback_query.message.edit_text(new_text, parse_mode="HTML")

    async def phone_numbers(self, message: types.Message):
        numbers = self.db.numbers.get_all()
        text = '☎️ Контакты:\n\n'

        for number in numbers:
            text += f'📞 {number.owner}: {number.number}\n'

        await message.answer(text)
