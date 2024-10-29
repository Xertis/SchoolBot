from aiogram import Router, F, types
from aiogram.filters import Command
from src.sql import AsyncSQL
from src.keyboards.reply_keyboard import BuildReplyButtons
from src.utils.no_command_callback import AddToNoCommand
#from src.state_machines.states import Class_state
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

classes_router = Router()
db = AsyncSQL('database.db')

class Class_state(StatesGroup):
    Class = State()

@classes_router.message(Command("classes"))
async def classes(message: types.Message, state: FSMContext):
    await state.set_state(Class_state.Class)
    await message.answer("Введите название класса\nПример:1А")


@classes_router.message(Class_state.Class)
async def classes_name(message: types.Message, state: FSMContext):
    text = message.text.upper()
    await state.update_data(Class=text)

    classes = await db.fetchall(f"SELECT name, teacher FROM classes WHERE name == '{text}'")

    if not classes:
        await message.answer(f"Класс {text} не найден, повторите запрос")
        return
    for Class in classes:
        if Class[1]:
            teacher = await db.fetchall(f"SELECT name FROM users WHERE id == {Class[1]}")
            if teacher:
                await message.answer(f"Руководитель: {teacher[0][0]}", parse_mode="Markdown")
        else:
            await message.answer(f"Руководитель не найден", parse_mode="Markdown")

    await state.clear()