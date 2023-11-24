from aiogram.fsm.state import State, StatesGroup


class GPTText(StatesGroup):
    text = State()
