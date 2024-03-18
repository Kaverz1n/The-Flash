from aiogram import Router, F
from aiogram.filters import MagicData
from aiogram.types import Message, CallbackQuery

maintenance_router = Router()
maintenance_router.message.filter(MagicData(F.maintenance_mode.is_(True)))


@maintenance_router.message()
async def maintenance_message(message: Message) -> None:
    '''
    A handler for the maintenance mode
    '''
    await message.answer('В настоящее время бот находится в режиме технического обслуживания\u00A0🔧')


@maintenance_router.callback_query()
async def maintenance_callback_query(callback: CallbackQuery) -> None:
    '''
    A handler for the maintenance mode
    '''
    await callback.message.answer('В настоящее время бот находится в режиме технического обслуживания\u00A0🔧')
