from aiogram.filters import BaseFilter
from aiogram.types import Message

from database.database_handlers.maintenance_mode import get_maintenance_mode_value


class MaintenanceModeFilter(BaseFilter):
    '''
    A filter for checking if the maintenance mode is enabled
    '''

    async def __call__(self, message: Message) -> bool:
        maintenance_mode_value = await get_maintenance_mode_value()

        return maintenance_mode_value
