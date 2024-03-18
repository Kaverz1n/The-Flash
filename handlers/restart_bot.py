from aiogram import Router, F
from aiogram.types import CallbackQuery

from database.database_handlers.admin import get_admins_telegram_ids
from keyboards.for_start import get_start_keyboard

router = Router()


@router.callback_query(F.data == 'restart_bot')
async def restart_bot(callback: CallbackQuery) -> None:
    '''
    A handler for restarting the bot
    '''
    user_id = callback.from_user.id
    admins_telegram_ids = await get_admins_telegram_ids()

    await callback.message.answer(
        text='TEST TEXT NUMBER TWO',
        reply_markup=get_start_keyboard(user_id=user_id, admins_telegram_ids=admins_telegram_ids)
    )

    await callback.answer(
        text='Бот успешно перезапущен\u00A0💖',
        show_alert=True
    )
