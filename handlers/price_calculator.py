from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.database_handlers.rates import get_rate_and_commission
from keyboards.for_back import get_back_keyboard
from keyboards.for_start import get_return_to_menu_keyboard
from states.price_calculator import PriceCalculatorState

router = Router()


@router.callback_query(StateFilter(None), F.data == 'price_calculator')
async def price_calculator(callback: CallbackQuery, state: FSMContext) -> None:
    '''
    A handler for calculating the good's price
    '''
    await state.clear()
    await callback.message.answer(
        text='💴\u00A0<b>КАЛЬКУЛЯТОР СТОИМОСТИ ТОВАРА</b>\u00A0💴\n\n'
             'Введите <b>цену товара в юанях</b>, чтобы наш бот рассчитал <b>полную</b> '
             'стоимость товара в <b>рублях</b> с учетом <b>комиссии</b> и <b>доставки</b> '
             'до <b>Москвы</b>:',
        reply_markup=get_back_keyboard(),
    )
    await callback.answer()
    await state.set_state(PriceCalculatorState.price)


@router.message(PriceCalculatorState.price, F.text.isdigit())
async def price_calculated(message: Message, state: FSMContext) -> None:
    '''
    A handler for showing converted good's price
    '''
    rate, commission = await get_rate_and_commission()

    if isinstance(rate, (int, float)) and isinstance(commission, (int, float)):
        full_price = int((int(message.text) * rate + commission))
        await message.answer(
            text='✅\u00A0<b>РАСЧЁТ ЦЕНЫ ТОВАРА ВЫПОЛНЕН</b>\u00A0✅\n\n'
                 f'Цена товара с учетом <b>комиссии</b> и <b>доставки</b> до '
                 f'<b>Москвы</b> в <b>рублях</b> составляет: <b>{full_price} руб.</b>',
            reply_markup=get_return_to_menu_keyboard(),
        )
    else:
        await message.answer(
            text='❌\u00A0<b>РАСЧЁТ ЦЕНЫ ТОВАРА НЕВЫПОЛНЕН</b>\u00A0❌\n\n'
                 'Произошла <b>ошибка</b> при расчёте <b>цены товара</b>. '
                 'Пожалуйста, <b>повторите попытку позже</b>.',
            reply_markup=get_return_to_menu_keyboard(),
        )

    await state.clear()


@router.message(PriceCalculatorState.price)
async def wrong_price_calculator_value(message: Message) -> None:
    '''
    A handler for showing an error message if the entered price is not integer
    '''
    await message.answer(
        text='❗<b>ОШИБКА</b>❗\n\n'
             'Пожалуйста, введите <b>действительное</b> и <b>целое</b> '
             'число цены товара в <b>юанях</b>:',
        reply_markup=get_return_to_menu_keyboard(),
    )
