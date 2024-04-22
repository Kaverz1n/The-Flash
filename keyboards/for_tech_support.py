from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_support_keyboard(tech_support_nickname: str) -> InlineKeyboardMarkup:
    '''
    A keyboard for tech support
    '''
    tech_support_buttons = [
        [InlineKeyboardButton(text='💌\u00A0Ответы на вопросы\u00A0💬', callback_data='answers_to_questions')],
        [InlineKeyboardButton(text='🤔\u00A0Как заказать?❓', callback_data='how_to_order')],
        [InlineKeyboardButton(text='🧑‍💻\u00A0Техподдержка\u00A0👩‍💻', url=f'https://t.me/{tech_support_nickname}')],
        [InlineKeyboardButton(text='Назад', callback_data='back')]
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=tech_support_buttons,
    )

    return keyboard
