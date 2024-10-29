from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from src.utils.no_command_callback import AddToNoCommand

async def BuildReplyButtons(buttons: list):
    for y, u in enumerate(buttons):
        for x, l in enumerate(u):
            buttons[y][x] = KeyboardButton(text=l[0])
            await AddToNoCommand(l[0], l[1], l[2])

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, input_field_placeholder='Выберите действие из меню', one_time_keyboard=True)