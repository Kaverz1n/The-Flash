import asyncio
import logging
import os

from aiogram import Bot, Dispatcher

from dotenv import load_dotenv

from handlers import maintenance_mode, start, about_company, answers_to_questions


async def main() -> None:
    '''
    An async main function to run the bot
    '''
    logging.basicConfig(level=logging.INFO)

    load_dotenv('.env')

    bot = Bot(token=os.getenv('BOT_TOKEN'), parse_mode='HTML')
    dispatcher = Dispatcher(maintenance_mode=False)

    dispatcher.include_router(maintenance_mode.maintenance_router)
    dispatcher.include_router(start.router)
    dispatcher.include_router(about_company.router)
    dispatcher.include_router(answers_to_questions.router)

    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
