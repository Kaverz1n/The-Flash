from aiogram.filters import BaseFilter
from aiogram.types import Message


class NotStartWith(BaseFilter):
    '''
    A filter for not starting with @
    '''

    async def __call__(self, message: Message) -> bool:
        return message.text[0] != '@'
