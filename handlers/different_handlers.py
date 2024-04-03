from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query(F.data == 'back')
async def back(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    '''
    A handler for to get back
    '''
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )
    await callback.answer()

    await state.clear()
