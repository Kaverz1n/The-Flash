import os

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_admin_panel_keyboard(maintenance_mode: bool, main_admin_telegram_id: int) -> ReplyKeyboardMarkup:
    '''
    A keyboard for the admin panel
    :param maintenance_mode: maintenance mode value
    :param main_admin_telegram_id: main admin telegram id
    '''
    buttons = [
        [KeyboardButton(text='📦\u00A0Текущие заказы\u00A0📦')],
        [KeyboardButton(text='💴\u00A0Изменить курс юаня\u00A0💴')],
        [KeyboardButton(text='💵\u00A0Изменить комиссию\u00A0💵')],
        [KeyboardButton(text='🥷\u00A0Добавить админа\u00A0🥷')],
    ]

    if main_admin_telegram_id == int(os.getenv('MAIN_ADMIN_TELEGRAM_ID')):
        buttons.append([KeyboardButton(text='🧟‍♂️\u00A0Удалить админа\u00A0🧟‍♂️')])

    if maintenance_mode:
        buttons.append([KeyboardButton(text='🔧\u00A0Выкл. режим тех.обслуживания\u00A0🔧')])
    else:
        buttons.append([KeyboardButton(text='🔧\u00A0Вкл. режим тех.обслуживания\u00A0🔧')])

    buttons.append([KeyboardButton(text='🚪\u00A0Выйти из админ. панели\u00A0🚪')])

    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder="Что делаем сегодня?"
    )

    return keyboard


def get_back_admin_keyboard() -> InlineKeyboardMarkup:
    '''
    A keyboard for back to the admin panel
    '''
    back_button = [
        [InlineKeyboardButton(text='Назад в админ. панель', callback_data='back_to_admin')]
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=back_button,
    )

    return keyboard
