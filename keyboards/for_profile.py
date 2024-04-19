from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_profile_keyboard(state=None) -> InlineKeyboardMarkup:
    '''
    A keyboard that consists of edit profile button and back to menu button
    '''
    buttons_data = {'Редактировать': 'edit_profile'}

    if state is not None:
        buttons_data['Вернуться в главное меню'] = 'return_main_menu'
    else:
        buttons_data['Назад'] = 'back'

    keyboard_builder = InlineKeyboardBuilder()

    for text, callback_data in buttons_data.items():
        keyboard_builder.button(text=text, callback_data=callback_data)

    keyboard_builder.adjust(1)

    return keyboard_builder.as_markup()


def get_edit_profile_keyboard(button_key=None) -> InlineKeyboardMarkup:
    '''
    A keyboard that consists of edit profile buttons
    :param button_key: name of the button to be removed
    '''
    buttons_data = {
        'Изменить имя': 'user_name', 'Изменить фамилию': 'user_surname',
        'Изменить отчество': 'user_patronymic', 'Изменить телефон': 'user_phone',
        'Изменить адрес': 'delivery_address',
    }

    if button_key is not None:
        buttons_data.pop(button_key)
        buttons_data['Сохранить'] = 'save_profile'
        buttons_data['Вернуться в главное меню'] = 'return_main_menu'
    else:
        buttons_data['Назад'] = 'back'

    keyboard_builder = InlineKeyboardBuilder()

    for text, callback_data in buttons_data.items():
        keyboard_builder.button(text=text, callback_data=callback_data)

    keyboard_builder.adjust(1)

    return keyboard_builder.as_markup()


def get_back_to_profile_keyboard() -> InlineKeyboardMarkup:
    '''
    A keyboard that consists of only one button to return to the profile
    '''
    back_button = [
        [InlineKeyboardButton(text='Вернуться в профиль', callback_data='profile')]
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=back_button,
    )

    return keyboard


def get_back_to_edit_keyboard() -> InlineKeyboardMarkup:
    '''
    A keyboard that consists of only one button to get back
    '''
    back_button = [
        [InlineKeyboardButton(text='Назад', callback_data='back_to_edit_profile')]
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=back_button,
    )

    return keyboard
