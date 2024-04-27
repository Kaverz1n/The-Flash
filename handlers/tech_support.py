import os
import random

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hide_link

from database.database_handlers.tech_support import get_tech_support_nicknames

from keyboards.for_tech_support import get_support_keyboard

router = Router()


@router.callback_query(F.data == 'tech_support')
async def tech_support(callback: CallbackQuery) -> None:
    '''
    A handler for showing tech support information
    '''
    tech_support_nicknames = random.choice(await get_tech_support_nicknames())

    await callback.message.answer(
        text=f'{hide_link(os.getenv("FULL_LOGO_URL"))}'
             f'🧑‍💻\u00A0<b>ТЕХНИЧЕСКАЯ ПОДДЕРЖКА</b>\u00A0👩‍💻\n\n'
             f'<b>Техническая поддержка</b> - команда <b>специалистов</b>, готовых '
             f'помочь вам в решении любых <b>проблем!</b>\n\n'
             f'Перед тем, как обратиться в <b>техподдержку</b>, полезно изучить раздел с '
             f'<b>ответами на часто задаваемые вопросы</b>, возможно, ваш вопрос '
             f'уже имеет <b>решение</b> там.\n\n'
             f'Если у вас возникают вопросы относительно <b>процесса заказа</b>, стоит обратить '
             f'внимание на <b>инструкцию по заказу</b> с подробным <b>видеопримером</b>.\n\n'
             f'Свяжитесь с нашей командой поддержки, нажав соответсвующую кнопку, или '
             f'по указанным ниже контактам:\n\n<b>E-mail:</b> theflash@gmail.com\n'
             f'<b>Администратор:</b> @Kaverz1n',
        reply_markup=get_support_keyboard(tech_support_nicknames)
    )
    await callback.answer()
