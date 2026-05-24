from aiogram.fsm.state import StatesGroup, State

class AdminState(StatesGroup):
    newsletter = State()

class UserState(StatesGroup):
    waiting_for_about_you = State()