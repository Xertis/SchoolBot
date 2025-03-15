from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def BuildInlineButtons(buttons: list):
    inline_keyboard = []

    for row in buttons:
        inline_row = []
        for button in row:
            inline_button = InlineKeyboardButton(
                text=button[0], callback_data=button[1])
            inline_row.append(inline_button)
        inline_keyboard.append(inline_row)

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
