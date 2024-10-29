from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

commands = {}
no_command = Router()

async def AddToNoCommand(text, command, if_state):
    commands[text.lower()] = (command, if_state)

@no_command.message(F.text.lower().in_(commands))
async def no_command_func(message: Message, state: FSMContext):
    msg = message.text.lower()
    if msg in commands.keys():
        if commands[msg][1] == True:
            await commands[msg][0](message, state)
        else:
            await commands[msg][0](message)
        return
    await no_command.next()(message, state)