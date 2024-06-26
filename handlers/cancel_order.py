import os

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hide_link

from keyboards.for_back import get_back_keyboard

router = Router()


@router.callback_query(F.data == 'cancel_order')
async def cancel_order(callback: CallbackQuery, state: FSMContext) -> None:
    '''
    A handler for showing the information about canceling the order
    '''
    await state.clear()

    await callback.message.answer(
        text=f'{hide_link(os.getenv("FULL_LOGO_URL"))}'
             f'📃\u00A0<b>ПОЛИТИКА ВОЗВРАТА ТОВАРА</b>\u00A0📃\n\n'
             f'Мы стремимся обеспечить <b>нашим покупателям</b> наилучшее <b>обслуживание</b>, '
             f'предоставляя возможность <b>возврата товара</b> в следующих случаях:\n\n'
             f'1. <b>Товар еще не был выкуплен нашей командой с маркетплейса POIZON(DEWU)</b>: '
             f'Если заказ еще <b>не был</b> обработан и оплачен нашей командой на маркетплейсе '
             f'<b>POIZON(DEWU)</b>, вы можете запросить <b>возврат средств</b>.\n\n'
             f'2. <b>Товар еще не был отправлен в Россию со склада в Китае</b>: '
             f'Если ваш заказ еще <b>не был</b> отправлен с нашего склада в <b>Китае</b>, '
             f'вы можете запросить <b>возврат средств</b>.\n\n'
             f'3. <b>Прошло более 35 дней с момента оплаты товара, а товар еще не был доставлен '
             f'на склад в России</b>: Если прошло более <b>35 дней</b> с момента <b>оплаты</b> '
             f'вашего заказа, а товар еще не был доставлен на наш склад в <b>России</b>, вы можете '
             f'запросить <b>возврат средств</b> или <b>дополнительную информацию</b> о статусе вашего заказа.\n\n'
             f'4. <b>Товар пришёл бракованный</b>: В случае получения <b>бракованного</b> '
             f'товара, мы готовы вернуть <b>30%</b> от стоимости товара и выдать '
             f'промокод <b>-15%</b> на следующий заказ.\n\n'
             f'5. <b>Товар был украден службой доставки</b>: Если вы столкнулись с ситуацией <b>кражи товара</b> '
             f'в процессе доставки, мы готовы предоставить вам полную <b>поддержку</b> в решении данной '
             f'проблемы с дальнейшим <b>возвратом денежных средств</b>.\n\n'
             f'Просим обратить внимание, что во всех случаях требуется обращение к нашей <b>тех. поддержке</b>, '
             f'для получения инструкций и помощи в <b>оформлении возврата</b>. '
             f'Вы можете связаться с нашей технической поддержкой нажав соответсвующую кнопку в главном меню, или '
             f'по указанным ниже контактам:\n\n<b>E-mail:</b> theflash@gmail.com\n'
             f'<b>Администратор:</b> @Kaverz1n',
        reply_markup=get_back_keyboard()
    )
    await callback.answer()
