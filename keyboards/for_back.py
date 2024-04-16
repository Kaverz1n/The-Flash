from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_back_keyboard() -> InlineKeyboardMarkup:
    '''
    A keyboard that consists of only one button to get back
    '''
    back_button = [
        [InlineKeyboardButton(text='Назад', callback_data='back')]
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=back_button,
    )

    return keyboard

