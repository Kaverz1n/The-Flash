from aiogram import Router
from aiogram.types import Message, CallbackQuery

from filters.admin_filter import NotAdminFilter
from filters.maintenance_mode_filter import MaintenanceModeFilter

maintenance_router = Router()


@maintenance_router.message(
    NotAdminFilter(),
    MaintenanceModeFilter()
)
async def maintenance_message(message: Message) -> None:
    '''
    A handler for the maintenance mode (message)
    '''
    await message.answer('В настоящее время бот находится в режиме технического обслуживания\u00A0🔧')


@maintenance_router.callback_query(
    NotAdminFilter(),
    MaintenanceModeFilter()
)
async def maintenance_callback_query(callback: CallbackQuery) -> None:
    '''
    A handler for the maintenance mode (callback_query)
    '''
    await callback.message.answer('В настоящее время бот находится в режиме технического обслуживания\u00A0🔧')
