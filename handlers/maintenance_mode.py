from aiogram import Router, F
from aiogram.filters import MagicData
from aiogram.types import Message

maintenance_router = Router()
maintenance_router.message.filter(MagicData(F.maintenance_mode.is_(True)))


@maintenance_router.message()
async def maintenance(message: Message) -> None:
    '''
    A handler for the maintenance mode
    '''
    await message.answer('В настоящее время бот находится в режиме технического обслуживания\u00A0🔧')
