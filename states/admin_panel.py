from aiogram.fsm.state import StatesGroup, State


class AdminPanelState(StatesGroup):
    '''
    A class including the state of the admin panel authentication
    '''
    password = State()
    authorized = State()


class AdminChangeRateState(StatesGroup):
    '''
    A class including the state of the changing rate
    '''
    rate = State()


class AdminChangeCommissionState(StatesGroup):
    '''
    A class including the state of the changing commission
    '''
    commission = State()


class AdminAddAdminState(StatesGroup):
    '''
    A class including the state of the adding admin
    '''
    admin_telegram_id = State()
    admin_password = State()


class AdminDeleteAdminState(StatesGroup):
    '''
    A class including the state of the deleting admin
    '''
    admin_telegram_id = State()
