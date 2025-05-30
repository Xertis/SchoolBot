from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


class WaitDocument(StatesGroup):
    Wait = State()

class WaitDocument2(StatesGroup):
    Wait = State()

class EventCreate(StatesGroup):
    EventName = State()
    EventDescription = State()
    EventTime = State()
    EventImage = State()
