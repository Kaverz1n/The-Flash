import os

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.for_back import get_back_keyboard

router = Router()


@router.callback_query(F.data == 'how_to_order')
async def how_to_order(callback: CallbackQuery, state: FSMContext) -> None:
    '''
    A handler for showing the information about ordering
    '''
    await state.clear()

    await callback.message.answer_video(
        video=os.getenv('HOW_TO_ORDER_VIDEO_ID'),
        caption=f'❓<b>КАК ЗАКАЗАТЬ?</b>❓\n\n'
                f'Для того чтобы <b>оформить заказ</b>, пожалуйста, перейдите в '
                f'<b>главное меню</b> и нажмите на кнопку <b>"Оформить заказ"</b>. '
                f'Затем следуйте <b>инструкция</b> на экране.\n\n'
                f'Если у Вас <b>возникли проблемы с заказом или оплатой</b>, свяжитесь '
                f'с нашей командой поддержки, нажав соответсвующую кнопку в главном меню, или '
                f'по указанным ниже контактам:\n\n<b>E-mail:</b> theflash@gmail.com\n'
                f'<b>Администратор:</b> @Kaverz1n',
        reply_markup=get_back_keyboard()
    )
    await callback.answer()
