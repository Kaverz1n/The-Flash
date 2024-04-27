from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

router = Router()


@router.callback_query(F.data == 'back')
async def back(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    '''
    A handler for to get back
    '''
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )
    await callback.answer()

    await state.clear()


@router.message(F.text)
async def different_text(message: Message) -> None:
    '''
    A handler for the different text
    '''
    await message.answer(
        text=f'<b>{message.text}</b> - звучит здорово!💖'
    )


@router.message(F.photo)
async def different_photo(message: Message) -> None:
    '''
    A handler for the different photo
    '''
    await message.answer(
        text=f'<b>Красивая</b> картинка!💖'
    )


@router.message(F.sticker)
async def different_sticker(message: Message) -> None:
    '''
    A handler for the different sticker
    '''
    await message.answer(
        text=f'Наклеем на <b>Вашу посылочку</b>!💖'
    )


@router.message(F.animation)
async def different_gif(message: Message) -> None:
    '''
    A handler for the different gif
    '''
    await message.answer(
        text='Бесконечность - <b>не предел</b>!💖'
    )


@router.message(F.document)
async def different_document(message: Message) -> None:
    '''
    A handler for the different document
    '''
    await message.answer(
        text='Обязательно <b>прочитаем</b>!💖'
    )


@router.message(F.location)
async def different_location(message: Message) -> None:
    '''
    A handler for the different location
    '''
    await message.answer(
        text='Обязательно Вас <b>навестим</b>!💖'
    )


@router.message(F.audio)
async def different_audio(message: Message) -> None:
    '''
    A handler for the different audio
    '''
    await message.answer(
        text='Обязательно <b>послушаем</b>!💖'
    )


@router.message(F.voice)
async def different_voice(message: Message) -> None:
    '''
    A handler for the different voice
    '''
    await message.answer(
        text='Какой обворожительный ангельский <b>голосок</b>!💖'
    )


@router.message(F.contact)
async def different_contact(message: Message) -> None:
    '''
    A handler for the different contact
    '''
    await message.answer(
        text='Обязательно <b>свяжемся</b>!💖'
    )


@router.message(F.poll)
async def different_poll(message: Message) -> None:
    '''
    A handler for the different poll
    '''
    await message.answer(
        text='Это <b>очень важный</b> опрос для нас!💖'
    )
