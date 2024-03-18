from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from database.database_handlers.admin import get_admins_telegram_ids
from keyboards.for_start import get_start_keyboard

router = Router()


@router.message(CommandStart())
async def start(message: Message) -> None:
    '''
    A handler for the /start command
    '''
    user_id = message.from_user.id
    admins_telegram_ids = await get_admins_telegram_ids()

    await message.answer(
        text='TEST TEXT',
        reply_markup=get_start_keyboard(user_id=user_id, admins_telegram_ids=admins_telegram_ids)
    )
