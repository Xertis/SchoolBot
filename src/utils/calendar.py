from datetime import datetime, timedelta
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def get_main_calendar_keyboard(current_date):
    left_button = InlineKeyboardButton(text="⬅️", callback_data=f"date_change:{current_date - timedelta(days=1)}")
    
    today = datetime.today().date()
    if current_date == today:
        date_text = "Сегодня"
    elif current_date == today - timedelta(days=1):
        date_text = "Вчера"
    elif current_date == today + timedelta(days=1):
        date_text = "Завтра"
    else:
        date_text = current_date.strftime("%d.%m.%Y")
    
    date_button = InlineKeyboardButton(text=date_text, callback_data="open_calendar")
    right_button = InlineKeyboardButton(text="➡️", callback_data=f"date_change:{current_date + timedelta(days=1)}")
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [left_button, date_button, right_button]
    ])
    
    return keyboard

async def get_calendar_keyboard(current_date):
    keyboard = []
    
    buttons = []
    for delta in range(-5, 6):
        date = current_date + timedelta(days=delta)
        date_button = InlineKeyboardButton(text=date.strftime("%d.%m"), callback_data=f"select_date:{date}")
        buttons.append(date_button)
    
    for i in range(0, len(buttons), 7):
        keyboard.append(buttons[i:i + 7])
    
    back_button = InlineKeyboardButton(text="Назад", callback_data="back_to_main")
    keyboard.append([back_button])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)