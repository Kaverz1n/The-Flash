from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_start_keyboard(user_id: int, admins_telegram_ids: list) -> InlineKeyboardMarkup:
    '''
    A keyboard that consists of the main buttons of the bot
    :param user_id: current user id
    :param admins_telegram_ids: list of admins' telegram ids
    '''
    buttons_data = {
        '🚚\u00A0ОФОРМИТЬ ЗАКАЗ\u00A0📦': 'to_order', '🤔\u00A0КАК ЗАКАЗАТЬ❓': 'how_to_order',
        '📬\u00A0ВОЗВРАТ ТОВАРА\u00A0📨': 'cancel_order', '🦹‍♀\u00A0️ПРОФИЛЬ\u00A0😌': 'profile',
        '💵\u00A0КАЛЬКУЛЯТОР СТОИМОСТИ\u00A0💴': 'price_calculator', '☀️\u00A0О КОМПАНИИ\u00A0🌈': 'about_company',
        '💌\u00A0ОТВЕТЫ НА ВОПРОСЫ\u00A0💬': 'answers_to_questions', '🧑‍💻\u00A0ТЕХПОДДЕРЖКА\u00A0👩‍💻': 'tech_support',
        '🌀\u00A0ПЕРЕЗАПУСК БОТА\u00A0🤖': 'restart_bot'
    }

    keyboard_builder = InlineKeyboardBuilder()

    for text, callback_data in buttons_data.items():
        keyboard_builder.button(text=text, callback_data=callback_data)

    if user_id in admins_telegram_ids:
        keyboard_builder.button(text='🥷\u00A0АДМИНКА\u00A0🥷', callback_data='to_admin_panel')

    keyboard_builder.adjust(1)

    return keyboard_builder.as_markup()


def get_return_to_menu_keyboard() -> InlineKeyboardMarkup:
    '''
    A keyboard that consists of only one button to return to the main menu
    '''
    back_button = [
        [InlineKeyboardButton(text='Вернуться в главное меню', callback_data='return_main_menu')]
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=back_button,
    )

    return keyboard
