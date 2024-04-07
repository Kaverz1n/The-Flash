from aiogram.fsm.state import StatesGroup, State


class ToOrderState(StatesGroup):
    '''
    A class including the states of the ordering
    '''
    order_url = State()
    order_photo = State()
    order_size = State()
    order_price = State()
