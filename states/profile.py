from aiogram.fsm.state import StatesGroup, State


class ProfileState(StatesGroup):
    '''
    A class including the states of the profile
    '''
    user_name = State()
    user_surname = State()
    user_patronymic = State()
    user_phone = State()
    delivery_address = State()
