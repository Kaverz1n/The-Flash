import os

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from database.database_handlers.admin import insert_admin_data, get_admins_telegram_ids, delete_from_admins, \
    select_admin_password
from database.database_handlers.maintenance_mode import get_maintenance_mode_value, set_maintenance_mode_value
from database.database_handlers.rates import get_rate_and_commission, update_rate, update_commission
from handlers.start import return_main_menu
from keyboards.for_admin_panel import get_admin_panel_keyboard, get_back_admin_keyboard
from keyboards.for_back import get_back_keyboard
from keyboards.for_start import get_return_to_menu_keyboard
from states.admin_panel import AdminPanelState, AdminChangeRateState, AdminChangeCommissionState, AdminAddAdminState, \
    AdminDeleteAdminState

router = Router()


@router.callback_query(F.data == 'admin_panel')
async def admin_panel(callback: CallbackQuery, state: FSMContext) -> None:
    '''
    A handler for the entering to admin panel
    '''
    await callback.message.answer(
        text='🥷\u00A0АВТОРИЗАЦИЯ\u00A0🥷\n\n'
             'Для входа в админ панель введите пароль:',
        reply_markup=get_back_keyboard()
    )

    await state.set_state(AdminPanelState.password)


@router.message(
    F.text,
    AdminPanelState.password
)
async def admin_password_received(message: Message, state: FSMContext) -> None:
    '''
    A handler for admin panel
    '''
    admin_telegram_id = message.from_user.id
    admin_password = await select_admin_password(admin_telegram_id)

    if message.text == admin_password:
        maintenance_mode = await get_maintenance_mode_value()
        await message.answer(
            text='🥷\u00A0АДМИН ПАНЕЛЬ\u00A0🥷\n\n'
                 'Вы вошли в админ панель. Что делаем сегодня: ',
            reply_markup=get_admin_panel_keyboard(maintenance_mode, message.from_user.id)
        )
        await state.set_state(AdminPanelState.authorized)
    else:
        await message.answer(
            text='❌\u00A0<b>ПРОИЗОШЛА ОШИБКА</b>\u00A0❌\n\n'
                 'Во время авторизации произошла ошибка. Пожалуйста, попробуйте еще раз:',
            reply_markup=get_return_to_menu_keyboard()
        )


@router.message(AdminPanelState.password)
async def wrong_admin_password(message: Message) -> None:
    '''
    A handler for wrong admin password
    '''
    await message.answer(
        text='❌\u00A0<b>ПРОИЗОШЛА ОШИБКА</b>\u00A0❌\n\n'
             'Во время авторизации произошла ошибка. Пожалуйста, попробуйте еще раз:',
        reply_markup=get_return_to_menu_keyboard()
    )


@router.message(
    F.text == '💴\u00A0Изменить курс юаня\u00A0💴',
    AdminPanelState.authorized
)
async def change_rate_admin(message: Message, state: FSMContext) -> None:
    '''
    A handler for changing the rate
    '''
    course = (await get_rate_and_commission())[0]

    await message.answer(
        text='💴\u00A0ИЗМЕНЕНИЕ КУРСА ЮАНЯ\u00A0💴\n\n'
             f'<b>Текущий курс юаня</b>: {round(course, 2)} руб.\n\n'
             f'Укажите новое значение:',
        reply_markup=get_back_admin_keyboard()
    )

    await state.set_state(AdminChangeRateState.rate)


@router.message(
    AdminChangeRateState.rate
)
async def rate_admin_received(message: Message, state: FSMContext) -> None:
    '''
    A handler for receiving the rate
    '''
    try:
        cny_rate = float(message.text)
        await update_rate(cny_rate)
        await state.set_state(AdminPanelState.authorized)
        await message.answer(
            text='✅\u00A0<b>КУРС ЮАНЯ УСПЕШНО ИЗМЕНЁН</b>\u00A0✅\n\n'
                 f'Курс юаня <b>изменён</b> и <b>составляет</b>: {round(cny_rate, 2)} руб.\n\n'
                 f'Вы можете продолжить работу в <b>админ. панели</b>, используя <b>специальные кнопки</b>.',

        )
    except:
        await message.answer(
            text='❌\u00A0<b>ПРОИЗОШЛА ОШИБКА</b>\u00A0❌\n\n'
                 'Во время ввода <b>нового</b> курса юаня произошла ошибка. '
                 'Пожалуйста, <b>попробуйте</b> еще раз:',
            reply_markup=get_back_admin_keyboard()
        )


@router.message(
    F.text == '💵\u00A0Изменить комиссию\u00A0💵',
    AdminPanelState.authorized
)
async def change_commission_admin(message: Message, state: FSMContext) -> None:
    '''
    A handler for changing the commission
    '''
    commission = (await get_rate_and_commission())[1]

    await message.answer(
        text='💵\u00A0ИЗМЕНЕНИЕ КОМИССИИ СЕРВИСА\u00A0💵\n\n'
             f'<b>Текущая комиссия сервиса</b>: {round(commission, 2)} руб.\n\n'
             f'Укажите новое значение:',
        reply_markup=get_back_admin_keyboard()
    )

    await state.set_state(AdminChangeCommissionState.commission)


@router.message(
    AdminChangeCommissionState.commission
)
async def commission_admin_received(message: Message, state: FSMContext) -> None:
    '''
    A handler for receiving the commission
    '''
    try:
        commission = float(message.text)
        await update_commission(commission)
        await state.set_state(AdminPanelState.authorized)
        await message.answer(
            text='✅\u00A0<b>КОМИССИЯ СЕРВИСА УСПЕШНО ИЗМЕНЕНА</b>\u00A0✅\n\n'
                 f'Комиссия сервиса <b>изменена</b> и <b>составляет</b>: {round(commission, 2)} руб.\n\n'
                 f'Вы можете продолжить работу в <b>админ. панели</b>, используя <b>специальные кнопки</b>.',
        )
    except:
        await message.answer(
            text='❌\u00A0<b>ПРОИЗОШЛА ОШИБКА</b>\u00A0❌\n\n'
                 'Во время ввода <b>новой</b> комиссии сервиса произошла ошибка. '
                 'Пожалуйста, <b>попробуйте</b> еще раз:',
            reply_markup=get_back_admin_keyboard()
        )


@router.message(
    F.text == '🥷\u00A0Добавить админа\u00A0🥷',
    AdminPanelState.authorized
)
async def add_telegram_id_admin(message: Message, state: FSMContext) -> None:
    '''
    A handler for adding a new admin's telegram ID
    '''
    await message.answer(
        text='🥷\u00A0ДОБАВЛЕНИЕ АДМИНИСТРАТОРА\u00A0🥷\n\n'
             f'Для добавления нового администратора введите его <b>телеграм ID</b>:',
        reply_markup=get_back_admin_keyboard()
    )

    await state.set_state(AdminAddAdminState.admin_telegram_id)


@router.message(
    F.text.isdigit(),
    AdminAddAdminState.admin_telegram_id
)
async def add_password_admin(message: Message, state: FSMContext) -> None:
    '''
    A handler for adding a new admin's password
    '''
    await state.update_data(admin_telegram_id=int(message.text))

    await message.answer(
        text='🥷\u00A0ДОБАВЛЕНИЕ АДМИНИСТРАТОРА\u00A0🥷\n\n'
             f'Для добавления нового администратора введите его <b>пароль</b>:',
        reply_markup=get_back_admin_keyboard()
    )

    await state.set_state(AdminAddAdminState.admin_password)


@router.message(
    AdminAddAdminState.admin_telegram_id
)
async def wrong_add_telegram_id_admin(message: Message) -> None:
    '''
    A handler for wrong admin's telegram ID
    '''
    await message.answer(
        text='❌\u00A0<b>ПРОИЗОШЛА ОШИБКА</b>\u00A0❌\n\n'
             'Во время ввода <b>телеграм ID</b> администратора произошла ошибка. '
             'Пожалуйста, <b>попробуйте</b> еще раз:',
        reply_markup=get_back_admin_keyboard()
    )


@router.message(
    F.text,
    AdminAddAdminState.admin_password
)
async def admin_data_received(message: Message, state: FSMContext) -> None:
    '''
    A handler for receiving admin data
    '''
    admin_data = await state.get_data()
    admin_telegram_id = admin_data['admin_telegram_id']
    admin_password = message.text

    await insert_admin_data(admin_telegram_id, admin_password)

    await message.answer(
        text='✅\u00A0<b>АДМИНИСТРАТОР ДОБАВЛЕН</b>\u00A0✅\n\n'
             f'Администратор успешно <b>добавлен</b> и может <b>авторизоваться</b>.\n\n'
             f'Вы можете продолжить работу в <b>админ. панели</b>, используя <b>специальные кнопки</b>.',
    )

    await state.set_state(AdminPanelState.authorized)


@router.message(
    AdminAddAdminState.admin_password
)
async def wrong_add_password_admin(message: Message) -> None:
    '''
    A handler for wrong admin's password
    '''
    await message.answer(
        text='❌\u00A0<b>ПРОИЗОШЛА ОШИБКА</b>\u00A0❌\n\n'
             'Во время ввода <b>пароля</b> администратора произошла ошибка. '
             'Пожалуйста, <b>попробуйте</b> еще раз:',
        reply_markup=get_back_admin_keyboard()
    )


@router.message(
    F.text == '🧟‍♂️\u00A0Удалить админа\u00A0🧟‍♂️',
    AdminPanelState.authorized
)
async def delete_admin(message: Message, state: FSMContext) -> None:
    '''
    A handler for deleting an admin
    '''
    await message.answer(
        text='🧟‍\u00A0УДАЛЕНИЕ АДМИНИСТРАТОРА\u00A0🧟‍\n\n'
             f'Для удаления администратора введите его <b>телеграм ID</b>:',
        reply_markup=get_back_admin_keyboard()
    )

    await state.set_state(AdminDeleteAdminState.admin_telegram_id)


@router.message(
    F.text.isdigit(),
    AdminDeleteAdminState.admin_telegram_id
)
async def delete_admin_data_received(message: Message, state: FSMContext) -> None:
    '''
    A handler for receiving admin data for deletion
    '''
    admin_telegram_id = int(message.text)
    admins_telegram_ids = await get_admins_telegram_ids()
    main_admin_telegram_id = os.getenv('MAIN_ADMIN_TELEGRAM_ID')

    # checking if the user is an admin and not the main admin
    if admin_telegram_id in admins_telegram_ids and admin_telegram_id != main_admin_telegram_id:
        await delete_from_admins(admin_telegram_id)

        await message.answer(
            text='✅\u00A0<b>АДМИНИСТРАТОР УДАЛЁН</b>\u00A0✅\n\n'
                 f'Администратор успешно <b>удалён</b> и не является частью <b>команды</b>.\n\n'
                 f'Вы можете продолжить работу в <b>админ. панели</b>, используя <b>специальные кнопки</b>.',
        )

        await state.set_state(AdminPanelState.authorized)

    else:
        await message.answer(
            text='❌\u00A0<b>ПРОИЗОШЛА ОШИБКА</b>\u00A0❌\n\n'
                 'Во время <b>удаления</b> администратора произошла ошибка. '
                 'Пожалуйста, <b>попробуйте</b> еще раз:',
            reply_markup=get_back_admin_keyboard()
        )


@router.message(
    AdminDeleteAdminState.admin_telegram_id
)
async def wrong_delete_admin_data(message: Message, state: FSMContext) -> None:
    '''
    A handler for wrong admin data
    '''
    await message.answer(
        text='❌\u00A0<b>ПРОИЗОШЛА ОШИБКА</b>\u00A0❌\n\n'
             'Во время <b>удаления</b> администратора произошла ошибка. '
             'Пожалуйста, <b>попробуйте</b> еще раз:',
        reply_markup=get_back_admin_keyboard()
    )


@router.message(
    F.text == '🔧\u00A0Вкл. режим тех.обслуживания\u00A0🔧',
    AdminPanelState.authorized
)
async def on_maintenance_mode(message: Message) -> None:
    '''
    A handler for turning on maintenance mode
    '''
    await set_maintenance_mode_value(True)

    await message.answer(
        text='🔧\u00A0<b>РЕЖИМ ТЕХ. ОБСЛУЖИВАНИЯ ВКЛЮЧЕН</b>\u00A0🔧\n\n'
             f'Режим тех.обслуживания <b>активирован</b>. Вы можете <b>выключить</b> '
             f'его в <b>админ. панели</b>.\n\n'
             f'Вы можете продолжить работу в <b>админ. панели</b>, используя <b>специальные кнопки</b>.',
        reply_markup=get_admin_panel_keyboard(maintenance_mode=True, main_admin_telegram_id=message.from_user.id)
    )


@router.message(
    F.text == '🔧\u00A0Выкл. режим тех.обслуживания\u00A0🔧',
    AdminPanelState.authorized
)
async def off_maintenance_mode(message: Message) -> None:
    '''
    A handler for turning off maintenance mode
    '''
    await set_maintenance_mode_value(False)

    await message.answer(
        text='🔧\u00A0<b>РЕЖИМ ТЕХ. ОБСЛУЖИВАНИЯ ВЫКЛЮЧЕН</b>\u00A0🔧\n\n'
             f'Режим тех.обслуживания <b>деактивирован</b>. Вы можете <b>включить</b> '
             f'его в <b>админ. панели</b>.\n\n'
             f'Вы можете продолжить работу в <b>админ. панели</b>, используя <b>специальные кнопки</b>.',
        reply_markup=get_admin_panel_keyboard(maintenance_mode=False, main_admin_telegram_id=message.from_user.id)
    )


@router.message(
    F.text == '🚪\u00A0Выйти из админ. панели\u00A0🚪',
    AdminPanelState.authorized
)
async def exit_admin_panel(message: Message, state: FSMContext) -> None:
    '''
    A handler for exiting the admin panel
    '''
    await message.answer(text='Выход...', reply_markup=ReplyKeyboardRemove())

    await return_main_menu(message, state)


@router.callback_query(
    F.data == 'back_to_admin',
)
async def back_to_admin(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    '''
    A handler for going back to the admin panel
    '''
    await state.set_state(AdminPanelState.authorized)

    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )

    await callback.message.answer(
        text='🥷\u00A0АДМИН ПАНЕЛЬ\u00A0🥷\n\n'
             'Вы можете продолжить работу в <b>админ. панели</b>, используя <b>специальные кнопки</b>.'
    )
    await callback.answer()
