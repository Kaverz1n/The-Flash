from aiogram.filters import BaseFilter
from aiogram.types import Message

from database.database_handlers.admin import get_admins_telegram_ids


class NotAdminFilter(BaseFilter):
    '''
    A filter for checking if the user is not an admin
    '''

    async def __call__(self, message: Message) -> bool:
        admins_telegram_ids = await get_admins_telegram_ids()
        user_telegram_id = message.from_user.id

        return user_telegram_id not in admins_telegram_ids
