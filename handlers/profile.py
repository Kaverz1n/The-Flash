from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.database_handlers.users import select_profile_data, update_profile_data
from keyboards.for_back import get_back_keyboard
from keyboards.for_profile import get_profile_keyboard, get_edit_profile_keyboard, get_back_to_profile_keyboard, \
    get_back_to_edit_keyboard
from keyboards.for_start import get_return_to_menu_keyboard
from states.profile import ProfileState
from utils import is_correct_address

router = Router()


@router.callback_query(F.data == 'profile')
async def profile(callback: CallbackQuery, state: FSMContext) -> None:
    '''
    A handler for showing user's profile data
    '''
    state = await state.get_state()
    user_telegram_id = callback.from_user.id
    profile_data = await select_profile_data(user_telegram_id)
    profile_filling = {}

    for data in profile_data:
        profile_filling[data] = '✅' if data != 'Не указан' else '❌'

    await callback.message.answer(
        text='🦹‍♀️\u00A0ВАШ ПРОФИЛЬ\u00A0🦹‍♀️\n\n'
             f'✅\u00A0<b>Id</b>: {user_telegram_id}\n'
             f'{profile_filling[profile_data[0]]}\u00A0<b>Имя</b>: {profile_data[0]}\n'
             f'{profile_filling[profile_data[1]]}\u00A0<b>Фамилия</b>: {profile_data[1]}\n'
             f'{profile_filling[profile_data[2]]}\u00A0<b>Отчество</b>: {profile_data[2]}\n'
             f'{profile_filling[profile_data[3]]}\u00A0<b>Телефон</b>: {profile_data[3]}\n'
             f'{profile_filling[profile_data[4]]}\u00A0<b>Адрес доставки</b>: {profile_data[4]}\n\n'
             f'<b>Текущих заказов</b>: {profile_data[5]}\n'
             f'<b>Выполненных заказов</b>: {profile_data[6]}\n'
             f'<b>Отмененных заказов</b>: {profile_data[7]}\n\n',
        reply_markup=get_profile_keyboard(state=state)
    )
    await callback.answer()


@router.callback_query(F.data == 'edit_profile')
async def edit_profile(callback: CallbackQuery, state: FSMContext) -> None:
    '''
    A handler for editing user's profile data
    '''
    await state.clear()

    await callback.message.answer(
        text='👶️\u00A0<b>РЕДАКТИРОВАНИЕ ПРОФИЛЯ</b>\u00A0👴️\n\n'
             'Для <b>изменения данных</b> вашего <b>профиля</b> выберите <b>кнопку</b>, '
             'отвечающую за изменение определенного <b>поля</b>. Вы можете изменить '
             '<b>одно</b> или <b>несколько</b> полей. Для <b>подтверждения</b> изменений '
             'нажмите кнопку <b>"Сохранить"</b>.',
        reply_markup=get_edit_profile_keyboard()
    )

    await callback.answer()


@router.callback_query(F.data == 'user_name')
async def user_name(callback: CallbackQuery, state: FSMContext) -> None:
    '''
    A handler for editing user's name
    '''
    await callback.message.answer(
        text='✏️\u00A0РЕДАКТИРОВАНИЕ ИМЕНИ\u00A0✏️\n\n'
             'Пожалуйста, введите Ваше <b>полное настоящее имя</b>. Оно необходимо '
             'для <b>оформления заказа</b>:',
        reply_markup=get_back_to_edit_keyboard()
    )
    await callback.answer()

    await state.set_state(ProfileState.user_name)


@router.message(
    ProfileState.user_name,
    F.text.isalpha(),
    F.text.len() <= 20
)
async def user_name_changed(message: Message, state: FSMContext) -> None:
    '''
    A handler for successful user's name change
    '''
    await state.update_data(user_name=message.text)

    await message.answer(
        text='✅\u00A0<b>ИМЯ УСПЕШНО ИЗМЕНЕНО</b>\u00A0✅\n\n'
             'Вы можете продолжить <b>редактирование</b> своих данных или <b>сохранить их</b>.',
        reply_markup=get_edit_profile_keyboard(button_key='Изменить имя')
    )


@router.message(ProfileState.user_name)
async def wrong_user_name_value(message: Message) -> None:
    '''
    A handler for showing an error message if the entered user's name is not alphabet
    '''
    await message.answer(
        text='❗<b>ОШИБКА</b>❗\n\n'
             'Введённое имя <b>некорректно</b>. Пожалуйста, <b>повторите попытку</b>:',
        reply_markup=get_back_to_profile_keyboard()
    )


@router.callback_query(F.data == 'user_surname')
async def user_surname(callback: CallbackQuery, state: FSMContext) -> None:
    '''
    A handler for editing user's surname
    '''
    await callback.message.answer(
        text='✏️\u00A0<b>РЕДАКТИРОВАНИЕ ФАМИЛИИ</b>\u00A0✏️\n\n'
             'Пожалуйста, введите Вашу <b>настоящую фамилию</b>. Она необходима '
             'для <b>оформления заказа</b>:',
        reply_markup=get_back_to_edit_keyboard()
    )
    await callback.answer()

    await state.set_state(ProfileState.user_surname)


@router.message(
    ProfileState.user_surname,
    F.text.isalpha(),
    F.text.len() <= 20
)
async def user_surname_changed(message: Message, state: FSMContext) -> None:
    '''
    A handler for successful user's surname change
    '''
    await state.update_data(user_surname=message.text)

    await message.answer(
        text='✅\u00A0<b>ФАМИЛИЯ УСПЕШНО ИЗМЕНЕНА</b>\u00A0✅\n\n'
             'Вы можете продолжить <b>редактирование</b> своих данных или <b>сохранить их</b>.',
        reply_markup=get_edit_profile_keyboard(button_key='Изменить фамилию')
    )


@router.message(ProfileState.user_surname)
async def wrong_user_surname_value(message: Message) -> None:
    '''
    A handler for showing an error message if the entered user's surname is not alphabet
    '''
    await message.answer(
        text='❗<b>ОШИБКА</b>❗\n\n'
             'Введённая фамилия <b>некорректна</b>. Пожалуйста, <b>повторите попытку</b>:',
        reply_markup=get_back_to_profile_keyboard()
    )


@router.callback_query(F.data == 'user_patronymic')
async def user_patronymic(callback: CallbackQuery, state: FSMContext) -> None:
    '''
    A handler for editing user's patronymic
    '''
    await callback.message.answer(
        text='✏️\u00A0<b>РЕДАКТИРОВАНИЕ ОТЧЕСТВА</b>\u00A0✏️\n\n'
             'Пожалуйста, введите Ваше <b>настоящее отчество</b>. Оно необходимо '
             'для <b>оформления заказа</b>:',
        reply_markup=get_back_to_edit_keyboard()
    )
    await callback.answer()

    await state.set_state(ProfileState.user_patronymic)


@router.message(
    ProfileState.user_patronymic,
    F.text.isalpha(),
    F.text.len() <= 20
)
async def user_patronymic_changed(message: Message, state: FSMContext) -> None:
    '''
    A handler for successful user's patronymic change
    '''
    await state.update_data(user_patronymic=message.text)

    await message.answer(
        text='✅\u00A0<b>ОТЧЕСТВО УСПЕШНО ИЗМЕНЕНО</b>\u00A0✅\n\n'
             'Вы можете продолжить <b>редактирование</b> своих данных или <b>сохранить их</b>.',
        reply_markup=get_edit_profile_keyboard(button_key='Изменить отчество')
    )


@router.message(ProfileState.user_patronymic)
async def wrong_user_patronymic_value(message: Message) -> None:
    '''
    A handler for showing an error message if the entered user's patronymic is not alphabet
    '''
    await message.answer(
        text='❗<b>ОШИБКА</b>❗\n\n'
             'Введённое отчество <b>некорректно</b>. Пожалуйста, <b>повторите попытку</b>:',
        reply_markup=get_back_to_profile_keyboard()
    )


@router.callback_query(F.data == 'user_phone')
async def user_phone(callback: CallbackQuery, state: FSMContext) -> None:
    '''
    A handler for editing user's phone
    '''
    await callback.message.answer(
        text='✏️\u00A0<b>РЕДАКТИРОВАНИЕ НОМЕРА ТЕЛЕФОНА</b>\u00A0✏️\n\n'
             'Пожалуйста, введите Ваш <b>текущий номер телефона</b> в формате '
             '<b>+79999999999</b>. Он необходим для <b>оформления заказа</b>:',
        reply_markup=get_back_to_edit_keyboard()
    )
    await callback.answer()

    await state.set_state(ProfileState.user_phone)


@router.message(
    ProfileState.user_phone,
    F.text.startswith('+'),
    F.text[1:].isdigit(),
    F.text.len() <= 15
)
async def user_phone_changed(message: Message, state: FSMContext) -> None:
    '''
    A handler for successful user's phone change
    '''
    await state.update_data(user_phone=message.text)

    await message.answer(
        text='✅\u00A0<b>НОМЕР ТЕЛЕФОНА УСПЕШНО ИЗМЕНЕН</b>\u00A0✅\n\n'
             'Вы можете продолжить <b>редактирование</b> своих данных или <b>сохранить их</b>.',
        reply_markup=get_edit_profile_keyboard(button_key='Изменить телефон')
    )


@router.message(ProfileState.user_phone)
async def wrong_user_phone_value(message: Message) -> None:
    '''
    A handler for showing an error message if the entered user's phone is not digits
    '''
    await message.answer(
        text='❗<b>ОШИБКА</b>❗\n\n'
             'Введённый номер телефона <b>некорректен</b>. Пожалуйста, <b>повторите попытку</b>:',
        reply_markup=get_back_to_profile_keyboard()
    )


@router.callback_query(F.data == 'delivery_address')
async def delivery_address(callback: CallbackQuery, state: FSMContext) -> None:
    '''
    A handler for editing user's delivery address
    '''
    await callback.message.answer(
        text='✏️\u00A0<b>РЕДАКТИРОВАНИЕ АДРЕСА ПУНКТА ВЫДАЧИ ЗАКАЗОВ</b>\u00A0✏️\n\n'
             'Пожалуйста, введите <b>адрес пункта выдачи заказов</b> в формате: '
             '<i>Почтовый индекс, страна, область, город, улица, дом</i> - <b>через запятую</b>. '
             'Он необходим для <b>оформления заказа</b>.\n\n'
             'Например: <i>248021, Россия, Калужская область, Калуга, Глаголева, 2А</i>\n\n'
             '<b>Введите адрес в соответствии с примером, без указания корпусов, строений и т.д. '
             'Кроме того, пожалуйста, следуйте примеру и оставьте все пробелы так, '
             'как они указаны.</b>\n\n'
             '<i>Указанный метод применим только для доставки в Россию. Если вы находитесь за '
             'пределами России, пожалуйста, свяжитесь с менеджером по контактным данным, '
             'указанным на странице о компании, или обратитесь в службу поддержки.</i>',
        reply_markup=get_back_to_edit_keyboard()
    )
    await callback.answer()

    await state.set_state(ProfileState.delivery_address)


@router.message(ProfileState.delivery_address, F.text.split(',').len() == 6)
async def delivery_address_changed(message: Message, state: FSMContext) -> None:
    '''
    A handler for successful delivery address change
    '''
    is_current_address = await is_correct_address(
        city_post_code=message.text.split(', ')[0],
        delivery_address=message.text
    )

    if is_current_address:
        await state.update_data(delivery_address=message.text)
        await message.answer(
            text='✅\u00A0<b>АДРЕС ПУНКТА ВЫДАЧИ ЗАКАЗОВ УСПЕШНО ИЗМЕНЕН</b>\u00A0✅\n\n'
                 'Вы можете продолжить <b>редактирование</b> своих данных или <b>сохранить их</b>.',
            reply_markup=get_edit_profile_keyboard(button_key='Изменить адрес')
        )
    else:
        await message.answer(
            text='❗<b>ПУНКТ ВЫДАЧИ CDEK НЕ НАЙДЕН</b>❗\n\n'
                 'Адрес пункта выдачи <b>CDEK</b>, введенный вами, <b>не был найден</b>. '
                 'Пожалуйста, убедитесь, что вы ввели <b>адрес</b> в соответствии с '
                 '<b>маской ввода</b>. Если вы уверены, что <b>адрес</b> введен '
                 '<b>корректно</b>, обратитесь в <b>службу поддержки</b> для решения проблемы.'
        )


@router.message(ProfileState.delivery_address)
async def wrong_delivery_address_value(message: Message) -> None:
    '''
    A handler for showing an error message if the entered delivery address is not correct
    '''
    await message.answer(
        text='❗<b>ОШИБКА</b>❗\n\n'
             'Введённый адрес пункта выдачи заказов <b>некорректен</b>. '
             'Пожалуйста, <b>повторите попытку</b>:',
        reply_markup=get_back_to_profile_keyboard()
    )


@router.callback_query(F.data == 'save_profile')
async def save_profile(callback: CallbackQuery, state: FSMContext) -> None:
    '''
    A handler for saving user's profile data
    '''
    user_telegram_id = callback.from_user.id
    user_nickname = callback.from_user.username

    profile_data = await select_profile_data(user_telegram_id)

    user_data = {
        'user_telegram_id': user_telegram_id,
        'user_nickname': user_nickname,
        'user_name': profile_data[0],
        'user_surname': profile_data[1],
        'user_patronymic': profile_data[2],
        'user_phone': profile_data[3],
        'delivery_address': profile_data[4],
    }

    saving_data = await state.get_data()

    for key, value in saving_data.items():
        user_data[key] = value

    await update_profile_data(**user_data)

    await callback.message.answer(
        text='✅\u00A0<b>ДАННЫЕ УСПЕШНО СОХРАНЕНЫ</b>\u00A0✅\n\n'
             'Ваши <b>новые данные</b> находятся в Вашем <b>профиле</b>. Вы можете '
             '<b>изменить</b> их <b>снова</b> в случае необходимости.',
        reply_markup=get_return_to_menu_keyboard(),
    )

    await callback.answer(
        text='Данные успешно сохранены\u00A0✏️',
        show_alert=True
    )


@router.callback_query(F.data == 'back_to_edit_profile')
async def back_to_edit_profile(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    '''
    A handler for to get back to edit the profile
    '''
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )
    await callback.answer()
