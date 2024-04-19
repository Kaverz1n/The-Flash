from aiogram.filters.callback_data import CallbackData


class OrderCallbackFactory(CallbackData, prefix='faborder'):
    '''
    A callback factory for the orders
    '''
    action: str
    order_id: int
    user_telegram_id: int
    user_chat_telegram_id: int