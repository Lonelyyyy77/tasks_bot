from aiogram.fsm.state import StatesGroup, State


class AddTask(StatesGroup):
    waiting_for_task_title = State()
    waiting_for_task_description = State()
    waiting_for_task_price = State()
