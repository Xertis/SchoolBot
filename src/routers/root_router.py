from aiogram import Router, F, types, Bot
from aiogram.filters import Command
from src.sql.db_api import DB
from src.utils.loader import LOADER
from src.utils.parsers import Parsers
from src.keyboards.inline_keyboard import BuildInlineButtons
from aiogram.fsm.context import FSMContext
from src.state_machines.states import WaitDocument, EventCreate
from src.routers.info_router import ShowEvents
from datetime import datetime
from src.utils.env import Constants
import os
import io


class FSM_eating:
    def __init__(self, root):
        self.root = root

        self.root.router.callback_query(F.data == "root.eating")(self.edit_eating_start)
        self.root.router.message(WaitDocument.Wait)(self.edit_eating_finish)

    async def edit_eating_start(
            self,
            callback_query: types.CallbackQuery,
            state: FSMContext):

        await state.set_state(WaitDocument.Wait)
        await callback_query.message.answer("Отправьте *.xlsx* таблицу с новым питанием", parse_mode="Markdown")
        await callback_query.answer()

    async def edit_eating_finish(
            self,
            message: types.Message,
            state: FSMContext,
            bot: Bot):

        if not message.document:
            await message.answer("Вы не отправили файл. Пожалуйста, отправьте *.xlsx* таблицу.", parse_mode="MarkDown")
            await state.clear()
            return

        document = message.document
        file = await bot.get_file(document.file_id)

        file_buffer = io.BytesIO()
        await bot.download_file(file.file_path, destination=file_buffer)

        file_buffer.seek(0)
        file_content = file_buffer.read()

        file_name = document.file_name
        date_str = file_name.split('-sm.xlsx')[0]
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        date = date_obj.strftime("%d.%m.%Y")

        eating_data = Parsers.eating.parse(file_content, is_path=False, date=date)

        if eating_data is False:
            await message.answer("Файл неверный. Пожалуйста, отправьте корректный *.xlsx* файл.", parse_mode="MarkDown")
            await state.clear()
            return

        eating_message = Parsers.eating.to_str(eating_data)

        for _, eat_data in eating_data.items():
            for meal, data in eat_data.items():
                dishes = data['блюда']
                for dish in dishes:
                    if dish["Раздел"] is None and dish["Блюдо"] is None:
                        continue
                    self.root.db.meal.add(
                        meal=meal,
                        category=dish["Раздел"],
                        recipe=dish["№ рец."],
                        dish=dish["Блюдо"],
                        grams=dish["Выход, г"],
                        price=data["цена"],
                        date=date_obj
                    )
            break
        await message.answer(eating_message, parse_mode="HTML")
        await message.answer(f"Питание обновлено.")
        await state.clear()


class FSM_events:
    def __init__(self, root):
        self.root = root

        self.root.router.callback_query(F.data == "root.events")(self.AskName)
        self.root.router.message(EventCreate.EventName)(self.AskDescription)
        self.root.router.message(EventCreate.EventDescription)(self.AskTime)
        self.root.router.message(EventCreate.EventTime)(self.AskImage)
        self.root.router.message(EventCreate.EventImage)(self.AskEnd)
        self.root.router.callback_query(F.data == "root.events.made")(self.AddEvent)
        self.root.router.callback_query(F.data == "root.events.del")(self.DeleteEvent)

    async def AskName(
            self,
            callback_query: types.CallbackQuery,
            state: FSMContext):

        await state.set_state(EventCreate.EventName)
        await callback_query.message.answer("Отправьте название мероприятия", parse_mode="Markdown")
        await callback_query.answer()

    async def AskDescription(
            self,
            message: types.Message,
            state: FSMContext):
        
        await state.update_data(name=message.text)
        await state.set_state(EventCreate.EventDescription)
        await message.answer("Отправьте описание мероприятия", parse_mode="Markdown")

    async def AskTime(
            self,
            message: types.Message,
            state: FSMContext):
        
        await state.update_data(description=message.text)
        await state.set_state(EventCreate.EventTime)
        await message.answer("Отправьте время проведения мероприятия", parse_mode="Markdown")

    async def AskImage(
            self,
            message: types.Message,
            state: FSMContext):

        date_string = message.text
        
        try:
            datetime_obj = datetime.strptime(date_string, Constants.DATE_FORMAT)
        except ValueError:
            await message.answer("Ошибка: Некорректный формат строки. Ожидается формат 'дд.мм.гггг чч:мм'.", parse_mode="Markdown")
            return
    
        await state.update_data(time=datetime_obj)
        await state.set_state(EventCreate.EventImage)
        await message.answer("Отправьте изображение мероприятия", parse_mode="Markdown")

    async def AskEnd(
            self,
            message: types.Message,
            state: FSMContext):
        
        photo = message.photo[-1]
    
        data = await state.get_data()
        time = data["time"].strftime(Constants.DATE_FORMAT)
        await message.answer("Результат:", parse_mode="Markdown")

        caption = f"""
🎈: *{data["name"]}*

{data["description"]}

⏰: _{time}_
        """

        y_or_n = [
            [['Добавить', "root.events.made"], ['Удалить', "root.events.del"]],
        ]

        await message.answer_photo(photo=photo.file_id, 
                                   caption=caption, 
                                   parse_mode="Markdown",
                                   reply_markup=await BuildInlineButtons(y_or_n))
        await state.update_data(photo_id=photo.file_id)

    async def AddEvent(
            self,
            callback_query: types.CallbackQuery,
            state: FSMContext,
            bot: Bot):
        
        if await state.get_state() != EventCreate.EventImage:
            return
        
        data = await state.get_data()
        photo_id = data.get("photo_id")

        file = await bot.get_file(photo_id)
        file_path = file.file_path

        index = LOADER.get_new_index()

        new_path = f"{LOADER.get_path() + str(index)}.jpg"
        await bot.download_file(file_path=file_path, destination=new_path)
        
        self.root.db.images.add(index)
        self.root.db.events.add(title = data["name"],
                                text = data["description"],
                                time = data["time"],
                                image = index
                                )
        
        await callback_query.message.answer("Мероприятие добавлено!")
        await state.clear()
        await callback_query.answer()

    async def DeleteEvent(
            self,
            callback_query: types.CallbackQuery,
            state: FSMContext):
        
        if await state.get_state() != EventCreate.EventImage:
            return
        
        await callback_query.message.answer("Мероприятие удалено!")
        await state.clear()
        await callback_query.answer()


class EventsRemover:
    def __init__(self, root):
        self.router = Router()
        self.root = root

        self.root.router.callback_query(F.data == "root.events.show_to_del")(self.Show)
        self.root.router.callback_query(F.data == "root.events.delete")(self.DeleteEvent)

    async def Show(self, message: types.Message):
        data = self.root.db.events.get_all()
        await ShowEvents("🎈 Мероприятия:", data, message)

    async def DeleteEvent(self, message: types.Message, bot: Bot):
        pass


class ROOT:
    def __init__(self):
        self.router = Router()
        self.db = DB()

        self.router.message(Command("root_help"))(self.help)
        self.eating = FSM_eating(self)
        self.events = FSM_events(self)

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
            [['Изменить питание', "root.eating"]],
            [['Добавить мероприятие', "root.events"]],
            [['Удалить мероприятие', "root.events.show_to_del"]]
        ]

        await message.answer("Выберите действие:", parse_mode="Markdown", reply_markup=await BuildInlineButtons(help))
