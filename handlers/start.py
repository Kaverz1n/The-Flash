import os

from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

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

    await message.answer_photo(
        photo=os.getenv('MAIN_PHOTO_ID'),
        caption='⚡\u00A0<b>THE FLASH</b>\u00A0⚡\n\n🌈\u00A0Мы – ваш лучший выбор '
                'для покупки <b>оригинальных</b> <b>брендовых</b> вещей из маркетплейса '
                'Poizon (dewu)\u00A0🌈\n\n 🌍\u00A0Наши склады в Китае и России обеспечивают '
                '<b>молниеносную</b> доставку товара как по территории России, так и по всему '
                'миру\u00A0🌍\n\n💴\u00A0<b>Минимальный курс юаня</b> и <b>минимальная комиссия '
                'сервиса</b> позволяют вам получать брендовые вещи по самым ⚡<b>ЗАРЯЖЕНЫМ</b>⚡ '
                'ценам\u00A0💴\n\n💖\u00A0Присоединяйтесь к <b>THE FLASH</b> и наслаждайтесь '
                'оригинальными товарами вместе с нами!\u00A0💖\n\n'
                '⚡\u00A0<b>БЫСТРО - НАДЁЖНО - МОЛНИЕНОСНО</b>\u00A0⚡',
        reply_markup=get_start_keyboard(user_id=user_id, admins_telegram_ids=admins_telegram_ids)
    )


@router.callback_query(F.data == 'restart_bot')
async def restart_bot(callback: CallbackQuery) -> None:
    '''
    A handler for restarting the bot
    '''
    user_id = callback.from_user.id
    admins_telegram_ids = await get_admins_telegram_ids()

    await callback.message.answer_photo(
        photo=os.getenv('MAIN_PHOTO_ID'),
        caption='⚡\u00A0<b>THE FLASH</b>\u00A0⚡\n\n💖\u00A0УДАЧНЫХ ПОКУПОК\u00A0💖',
        reply_markup=get_start_keyboard(user_id=user_id, admins_telegram_ids=admins_telegram_ids)
    )

    await callback.answer(
        text='Бот успешно перезапущен\u00A0💖',
        show_alert=True
    )


@router.callback_query(F.data == 'back_to_menu')
async def back_to_menu(callback: CallbackQuery, bot: Bot) -> None:
    '''
    A handler for to back to main menu
    '''
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )
