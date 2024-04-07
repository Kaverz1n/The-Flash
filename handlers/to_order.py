import os

from aiogram import Router, F, Bot
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, LabeledPrice, PreCheckoutQuery
from aiogram.utils.media_group import MediaGroupBuilder
from aiohttp import ClientSession, InvalidURL

from database.database_handlers.orders import insert_order_data
from database.database_handlers.rates import get_course_and_commission
from database.database_handlers.users import select_profile_data, select_user_pk, increase_current_orders
from keyboards.for_profile import get_profile_keyboard
from keyboards.for_start import get_return_to_menu_keyboard
from keyboards.for_to_order import get_familiarizing_keyboard, get_start_order_keyboard, get_confirm_order_keyboard, \
    get_payment_keyboard
from states.to_order import ToOrderState

router = Router()


@router.callback_query(F.data == 'to_order')
async def to_order(callback: CallbackQuery, state: FSMContext) -> None:
    '''
    An async function to familiarize
    '''
    await state.clear()

    await callback.message.answer(
        text='Перед <b>оформлением заказа</b>, пожалуйста, ознакомьтесь '
             'с соответсвующей <b>инструкцией</b>:',
        reply_markup=get_familiarizing_keyboard()
    )

    await callback.answer()


@router.callback_query(F.data == 'familiarized')
async def familiarized(callback: CallbackQuery, state: FSMContext) -> None:
    '''
    An async function to start ordering
    '''
    await state.clear()

    user_telegram_id = callback.from_user.id
    user_data = await select_profile_data(user_telegram_id)

    if not 'Не указан' in tuple(user_data):
        album_builder = MediaGroupBuilder(
            caption='📦\u00A0ССЫЛКА НА ТОВАР\u00A0📦️\n\n'
                    'Пожалуйста, укажите <b>ссылку на товар с POIZON (DEWU)</b>, '
                    'который вы хотите заказать в следующем формате:\n\n'
                    '<i>https://dw4.co/t/A/XXXXXXXX</i>\n\n'
                    '<i>Для корректного получения <b>ссылки</b>, пожалуйста, следуйте '
                    '<b>инструкции</b> на <b>скриншотах.</b></i>',
        )
        photo_url_list = [
            'https://telegra.ph/file/549a4e00bd95287cff2d2.png',
            'https://telegra.ph/file/3836e44c12a17859d3803.png',
            'https://telegra.ph/file/946bcb6282c5de5c03336.png'
        ]

        for photo_url in photo_url_list:
            album_builder.add_photo(media=photo_url)

        await callback.message.answer_media_group(
            media=album_builder.build(),
            reply_markup=get_start_order_keyboard()
        )

        await state.set_state(ToOrderState.order_url)
    else:
        await callback.message.answer(
            text='❌\u00A0<b>ПРОФИЛЬ НЕ ЗАПОЛНЕН</b>\u00A0❌\n\n'
                 'Ваш <b>профиль</b> не заполнен. Пожалуйста, укажите <b>действийные</b> '
                 'данные, ведь они необходимы для <b>оформления заказа!</b>',
            reply_markup=get_profile_keyboard()
        )

    await callback.answer()


@router.message(ToOrderState.order_url)
async def order_url_received(message: Message, state: FSMContext) -> None:
    '''
    An async function to check the order url
    '''
    try:
        entities = message.entities or []
        user_url = [item.extract_from(message.text) for item in entities if item.type == 'url'][0]

        if not 'https://dw4.co' in user_url:
            raise InvalidURL

        async with ClientSession() as session:
            async with session.get(url=user_url) as response:
                status = response.status

        if status == 200:
            await state.update_data(order_url=user_url)

            album_builder = MediaGroupBuilder(
                caption='📸\u00A0ФОТО ТОВАРА\u00A0📸\n\n'
                        'Пожалуйста, прикрепите текущие <b>главное фото товара с POIZON (DEWU)</b>, '
                        'который вы хотите заказать.\n\n'
                        '<i>Для корректного получения <b>фото</b>, пожалуйста, следуйте '
                        '<b>инструкции</b> на <b>скриншотах.</b></i>',
            )
            photo_url_list = [
                'https://telegra.ph/file/12c8621e3564d8f6b8db0.png',
                'https://telegra.ph/file/44fc1c5234b526bab0e07.png',
                'https://telegra.ph/file/618617d9b7b5691821547.png'
            ]

            for photo_url in photo_url_list:
                album_builder.add_photo(media=photo_url)

            await message.answer_media_group(
                media=album_builder.build(),
                reply_markup=get_start_order_keyboard()
            )

            await state.set_state(ToOrderState.order_photo)
        else:
            raise InvalidURL
    except:
        await message.answer(
            text='❌\u00A0<b>ПРОИЗОШЛА ОШИБКА</b>\u00A0❌\n\n'
                 'Указана <b>недействительная</b> ссылка. Возможно, присутствуют '
                 '<b>лишние</b> пробелы или символы. Пожалуйста, убедитесь в правильности '
                 'ссылки и введите её согласно <b>предоставленному шаблону</b>.',
            reply_markup=get_start_order_keyboard()
        )


@router.message(
    ToOrderState.order_photo,
    F.photo
)
async def order_photo_received(message: Message, state: FSMContext) -> None:
    '''
    An async function to receive the order photo
    '''
    await state.update_data(order_photo=message.photo[-1].file_id)

    album_builder = MediaGroupBuilder(
        caption='📸\u00A0РАЗМЕР ТОВАРА\u00A0📸\n\n'
                'Пожалуйста, укажите необходимый <b>размер товара с POIZON (DEWU)</b>, '
                'который вы хотите заказать.\n\n'
                '<i>Для корректного получения <b>размера</b>, пожалуйста, следуйте '
                '<b>инструкции</b> на <b>скриншотах.</b></i>'
    )
    photo_url_list = [
        'https://telegra.ph/file/a39274118a87db7937a20.png',
        'https://telegra.ph/file/252d52a9befb403186809.png',
    ]

    for photo_url in photo_url_list:
        album_builder.add_photo(media=photo_url)

    await message.answer_media_group(
        media=album_builder.build(),
        reply_markup=get_start_order_keyboard()
    )

    await state.set_state(ToOrderState.order_size)


@router.message(
    ToOrderState.order_photo
)
async def wrong_order_photo(message: Message) -> None:
    '''
    An async function to handle wrong order photo
    '''
    await message.answer(
        text='❌\u00A0<b>ПРОИЗОШЛА ОШИБКА</b>\u00A0❌\n\n'
             'Пожалуйста, прикрепите <b>действительное фото товара</b> с <b>POIZON (DEWU)</b>.',
        reply_markup=get_start_order_keyboard()
    )


@router.message(
    ToOrderState.order_size,
    F.text.len() <= 10
)
async def order_size_received(message: Message, state: FSMContext) -> None:
    '''
    An async function to receive the order size
    '''
    await state.update_data(order_size=message.text)

    album_builder = MediaGroupBuilder(
        caption='💴\u00A0ЦЕНА ТОВАРА В ЮАНЯХ\u00A0💴\n\n'
                'Пожалуйста, укажите подходящую <b>цену товара с POIZON (DEWU)</b>, '
                'который вы хотите заказать.\n\n'
                '<i>Для корректного получения <b>цены</b>, пожалуйста, следуйте '
                '<b>инструкции</b> на <b>скриншотах.</b></i>\n\n'
                '<b><u>ВАЖНО:</u>ТОВАРЫ С ЗНАКОМ ≈ НЕ ПРИНИМАЮТСЯ К ПОКУПКЕ. КРОМЕ '
                'ТОГО, МЫ ПРИНИМАЕМ ТОВАРЫ ТОЛЬКО ПО ЦЕНЕ, УКАЗАННОЙ НА ЦЕННИКЕ С '
                'ЗАЧЕРКНУТОЙ ЦЕНОЙ.</b>'
    )
    photo_url_list = [
        'https://telegra.ph/file/edc832ea4a5988f75e09a.png',
        'https://telegra.ph/file/0827b05ded8b4e2b368b5.png',
    ]

    for photo_url in photo_url_list:
        album_builder.add_photo(media=photo_url)

    await message.answer_media_group(
        media=album_builder.build(),
        reply_markup=get_start_order_keyboard()
    )

    await state.set_state(ToOrderState.order_price)


@router.message(ToOrderState.order_size)
async def wrong_order_size(message: Message) -> None:
    '''
    An async function to handle wrong order size
    '''
    await message.answer(
        text='❌\u00A0<b>ПРОИЗОШЛА ОШИБКА</b>\u00A0❌\n\n'
             'Пожалуйста, укажите <b>действительный размер товара</b> '
             'с <b>POIZON (DEWU)</b>.',
        reply_markup=get_start_order_keyboard()
    )


@router.message(
    ToOrderState.order_price,
    F.content_type != ContentType.SUCCESSFUL_PAYMENT,
    F.text.isdigit()
)
async def order_price_received(message: Message, state: FSMContext) -> None:
    '''
    An async function to receive the order price
    '''
    order_data = await state.get_data()
    user_data = await select_profile_data(message.from_user.id)
    rate, commission = await get_course_and_commission()

    if isinstance(rate, (int, float)) and isinstance(commission, (int, float)):
        full_price = int((int(message.text) * rate + commission))

        await message.answer_photo(
            photo=order_data['order_photo'],
            caption=f'📬\u00A0ИНФОРМАЦИЯ О ЗАКАЗЕ\u00A0📬\n\n'
                    f'<b>Ссылка на товар:</b> {order_data["order_url"]}\n'
                    f'<b>Размер товара:</b> {order_data["order_size"]}\n'
                    f'<b>Цена товара в юанях:</b> {message.text} юан.\n'
                    f'<b>Цена товара в рублях:</b> {full_price} руб.\n\n'
                    f'🦹‍♀️\u00A0ИНФОРМАЦИЯ О ПОЛУЧАТЕЛЕ\u00A0🦹‍♀️\n\n'
                    f'<b>ФИО:</b> {user_data[1]} {user_data[0]} {user_data[2]}\n'
                    f'<b>Телефон:</b> {user_data[3]}\n'
                    f'<b>Адрес доставки:</b> {user_data[4]}\n\n'
                    f'<i>Если данные о товаре и получателе верны, пожалуйста, '
                    f'нажмите кнопку "Подтвердить" и следуйте дальнейшим инструкциям.</i>\n\n'
                    f'Если у Вас <b>возникли проблемы с заказом или оплатой</b>, свяжитесь '
                    f'с нашей командой поддержки, нажав соответсвующую кнопку в главном меню, или '
                    f'по указанным ниже контактам:\n\n<b>E-mail:</b> theflash@gmail.com\n'
                    f'<b>Администратор:</b> @Kaverz1n',
            reply_markup=get_confirm_order_keyboard(),
        )

        await state.update_data(yuan_price=int(message.text))
        await state.update_data(rub_price=full_price)

    else:
        await message.answer(
            text='❌\u00A0<b>РАСЧЁТ ЦЕНЫ ТОВАРА НЕВЫПОЛНЕН</b>\u00A0❌\n\n'
                 'Произошла <b>ошибка</b> при расчёте <b>цены товара</b>. '
                 'Пожалуйста, <b>повторите попытку позже</b>.',
            reply_markup=get_return_to_menu_keyboard(),
        )


@router.message(
    ToOrderState.order_price,
    F.content_type != ContentType.SUCCESSFUL_PAYMENT
)
async def wrong_order_price(message: Message) -> None:
    '''
    An async function to handle wrong order price
    '''
    await message.answer(
        text='❌\u00A0<b>ПРОИЗОШЛА ОШИБКА</b>\u00A0❌\n\n'
             'Пожалуйста, укажите <b>действительное и целое число цены товара в юанях</b> '
             'с <b>POIZON (DEWU)</b>.',
        reply_markup=get_start_order_keyboard()
    )


@router.callback_query(F.data == 'confirm_order')
async def confirm_order(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    '''
    An async function to pay for an order
    '''
    order_data = await state.get_data()

    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title='⚡\u00A0Заказ с POIZON by THE FLASH\u00A0⚡',
        description='Для оплаты вашего заказа, пожалуйста, воспользуйтесь соответствующей кнопкой. '
                    'После успешной оплаты ваш заказ немедленно будет передан '
                    'нашей команде для обработки!\n\n'
                    '💖\u00A0Спасибо, что выбираете нас!\u00A0\u00A0💖\n\n'
                    '⚡Быстро - Надёжно - Молниеносно⚡',
        provider_token=os.getenv('PAYMENT_PROVIDER_TOKEN'),
        currency='rub',
        prices=[
            LabeledPrice(
                label='⚡\u00A0Заказ с POIZON by THE FLASH\u00A0⚡',
                amount=order_data['rub_price'] * 10
            )
        ],
        max_tip_amount=500 * 100,
        suggested_tip_amounts=[100 * 100, 200 * 100, 300 * 100, 400 * 100],
        start_parameter='TheFlash',
        provider_data=None,
        photo_url=os.getenv('FULL_LOGO_URL'),
        photo_size=512,
        photo_width=512,
        photo_height=512,
        need_name=False,
        need_phone_number=False,
        need_email=False,
        need_shipping_address=False,
        send_phone_number_to_provider=False,
        send_email_to_provider=False,
        is_flexible=False,
        disable_notification=False,
        protect_content=True,
        reply_to_message_id=None,
        allow_sending_without_reply=True,
        reply_markup=get_payment_keyboard(),
        request_timeout=15,
        payload='the_flash_invoice',

    )


@router.pre_checkout_query()
async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot) -> None:
    '''
    An async function to handle pre checkout query
    '''
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@router.message(
    ToOrderState.order_price,
    F.content_type == ContentType.SUCCESSFUL_PAYMENT
)
async def successful_payment(message: Message, state: FSMContext) -> None:
    '''
    An async function to show successful payment message
    '''
    user_pk = await select_user_pk(user_telegram_id=message.from_user.id)
    order_data = await state.get_data()

    await state.clear()

    await insert_order_data(
        order_url=order_data['order_url'], yuan_price=order_data['yuan_price'],
        rub_price=order_data['rub_price'], order_photo_id=order_data['order_photo'],
        order_size=order_data['order_size'], user_id=user_pk[0],
        chat_telegram_id=message.chat.id
    )

    await increase_current_orders(message.from_user.id)

    await message.answer(
        text='🧾\u00A0ВАШ ЗАКАЗ ОПЛАЧЕН\u00A0🧾\n\n'
             'Наша команда в <b>Китае</b> скоро выкупит товар с <b>POIZON (DEWU)</b> '
             'и отправит его в <b>Россию</b>. Как только товар будет отправлен из <b>Москвы</b> '
             'на ваш адрес пункта получения <b>СДЭК</b>, вы получите <b>трек-номер</b>.\n\n'
             '💖\u00A0Спасибо, что выбираете нас!\u00A0\u00A0💖\n\n'
             '⚡Быстро - Надёжно - Молниеносно⚡',
        reply_markup=get_return_to_menu_keyboard()
    )
