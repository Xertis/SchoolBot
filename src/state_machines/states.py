from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


class Date_Class_state(StatesGroup):
    Date = State()
    Class = State()

class Class_state(StatesGroup):
    Class = State()

class Date_state(StatesGroup):
    Date = State()