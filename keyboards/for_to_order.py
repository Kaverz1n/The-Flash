from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_familiarizing_keyboard() -> InlineKeyboardMarkup:
    '''
    A keyboard that consists of one button to familiarize with the ordering
    '''
    button = [
        [InlineKeyboardButton(text='✅\u00A0Я ознакомился\u00A0✅', callback_data='familiarized')]
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=button,
    )

    return keyboard


def get_start_order_keyboard() -> InlineKeyboardMarkup:
    '''
    A keyboard that consists of two buttons: to start ordering and to return to the main menu
    '''
    buttons = [
        [InlineKeyboardButton(text='Начать заказ сначала', callback_data='familiarized')],
        [InlineKeyboardButton(text='Вернуться в главное меню', callback_data='return_main_menu')]
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )

    return keyboard


def get_confirm_order_keyboard() -> InlineKeyboardMarkup:
    '''
    A keyboard that consists of two buttons: to confirm the order and to start ordering again
    '''
    buttons = [
        [InlineKeyboardButton(text='✅\u00A0Подтвердить\u00A0✅', callback_data='confirm_order')],
        [InlineKeyboardButton(text='Начать заказ сначала', callback_data='familiarized')],
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )

    return keyboard


def get_payment_keyboard() -> InlineKeyboardMarkup:
    '''
    A keyboard that consists of one button to pay
    '''
    button = [
        [InlineKeyboardButton(text='Оплатить\u00A0💳', pay=True)]
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=button,
    )

    return keyboard