from aiogram import Bot, types

handlers = {}


async def register_callback(callback_name: str, handler: function):
    handlers[callback_name] = handler


async def handle_callback(callback_query: types.CallbackQuery):
    callback_name = callback_query.data
    await callback_query.answer()

    if callback_name:
        handlers[callback_name](callback_query)
