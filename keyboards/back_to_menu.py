from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_back_to_menu_keyboard() -> InlineKeyboardMarkup:
    '''
    A keyboard that consists of only one button to back to main menu
    '''
    back_button = [
        [InlineKeyboardButton(text='Назад', callback_data='back_to_menu')]
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=back_button,
    )

    return keyboard
