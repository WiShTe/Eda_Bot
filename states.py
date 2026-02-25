from aiogram.fsm.state import State, StatesGroup


class Add_meal(StatesGroup):
    name = State()
    inrdients = State()
    reciept = State()
    time_of_meal = State()
    confirmation = State()