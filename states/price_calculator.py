from aiogram.fsm.state import StatesGroup, State


class PriceCalculatorState(StatesGroup):
    '''
    A class including the states of the price calculator
    '''
    price = State()
