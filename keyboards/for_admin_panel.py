import os

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_factories.order_factory import OrderCallbackFactory


def get_admin_panel_keyboard(maintenance_mode: bool, admin_telegram_id: int) -> ReplyKeyboardMarkup:
    '''
    A keyboard for the admin panel
    :param maintenance_mode: maintenance mode value
    :param admin_telegram_id: admin telegram id
    '''
    buttons = [
        [KeyboardButton(text='📦\u00A0Просмотреть заказы\u00A0📦')],
        [KeyboardButton(text='💴\u00A0Изменить курс юаня\u00A0💴')],
        [KeyboardButton(text='💵\u00A0Изменить комиссию\u00A0💵')],
        [KeyboardButton(text='🥷\u00A0Добавить админа\u00A0🥷')],
    ]

    if admin_telegram_id == int(os.getenv('MAIN_ADMIN_TELEGRAM_ID')):
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


def get_check_orders_keyboard() -> ReplyKeyboardMarkup:
    '''
    A keyboard for checking orders
    '''
    buttons = [
        [KeyboardButton(text='🗂️\u00A0Получить данные о заказах\u00A0🗂️')],
        [KeyboardButton(text='🛒\u00A0Получить данные по заказу\u00A0🛒')],
        [KeyboardButton(text='🥷\u00A0Назад в админ. панель\u00A0🥷')]
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder='Выберите опцию'
    )

    return keyboard


def change_order_status_keyboard(
        order_status: str,
        order_id: int,
        user_telegram_id: int,
        user_chat_telegram_id: int
) -> InlineKeyboardMarkup:
    '''
    A keyboard for changing order status
    '''
    builder = InlineKeyboardBuilder()

    if order_status == 'Создан':
        builder.button(
            text='Отправлен',
            callback_data=OrderCallbackFactory(
                action='отправить', order_id=order_id,
                user_telegram_id=user_telegram_id,
                user_chat_telegram_id=user_chat_telegram_id
            )
        ),
        builder.button(
            text='Отменён',
            callback_data=OrderCallbackFactory(
                action='отменить', order_id=order_id,
                user_telegram_id=user_telegram_id,
                user_chat_telegram_id=user_chat_telegram_id
            )
        ),

    builder.button(text='Назад в админ. панель', callback_data='back_to_admin')

    builder.adjust(1)

    return builder.as_markup()


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
