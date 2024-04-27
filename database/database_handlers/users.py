import asyncpg

from database.database_settings.database_data import get_database_data


async def update_profile_data(
        user_nickname: str, user_name: str, user_surname: str,
        user_patronymic: str, user_phone: str, delivery_address: str,
        user_telegram_id: int
) -> None:
    '''
    An async function to update profile data in the users table
    :param user_nickname: user's telegram nickname
    :param user_name: user's real name
    :param user_surname: user's real surname
    :param user_patronymic: user's real patronymic
    :param user_phone: user's current phone
    :param delivery_address: user's current delivery address
    :param user_telegram_id: user's telegram id
    '''
    database_data = get_database_data()
    connection = await asyncpg.connect(**database_data)

    await connection.execute(
        'UPDATE users SET user_nickname = $1, user_name = $2, '
        'user_surname = $3, user_patronymic = $4, user_phone = $5, '
        'delivery_address = $6 WHERE user_telegram_id = $7;',
        user_nickname, user_name, user_surname, user_patronymic,
        user_phone, delivery_address, user_telegram_id
    )


async def insert_profile_data(
        user_telegram_id: int, user_nickname: str,
        user_name: str = 'Не указан', user_surname: str = 'Не указан',
        user_patronymic: str = 'Не указан', user_phone: str = 'Не указан',
        delivery_address: str = 'Не указан', current_orders: int = 0,
        completed_orders: int = 0, canceled_orders: int = 0
) -> None:
    '''
    An async function to insert profile data into the users table
    :param user_telegram_id: user's telegram id
    :param user_nickname: user's telegram nickname
    :param user_name: user's real name
    :param user_surname: user's real surname
    :param user_patronymic: user's real patronymic
    :param user_phone: user's current phone
    :param delivery_address: user's current delivery address
    :param current_orders: user's current orders
    :param completed_orders: user's completed orders
    :param canceled_orders: user's canceled orders
    '''
    database_data = get_database_data()
    connection = await asyncpg.connect(**database_data)

    await connection.execute(
        'INSERT INTO users (user_telegram_id, user_nickname, '
        'user_name, user_surname, user_patronymic, user_phone, '
        'delivery_address, current_orders, completed_orders, '
        'canceled_orders) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)',
        user_telegram_id, user_nickname, user_name, user_surname,
        user_patronymic, user_phone, delivery_address, current_orders,
        completed_orders, canceled_orders
    )

    await connection.close()


async def select_profile_data(user_telegram_id: int) -> tuple:
    '''
    An async function to select profile data from the users table
    :param user_telegram_id: user's telegram id
    '''
    database_data = get_database_data()
    connection = await asyncpg.connect(**database_data)

    result = await connection.fetch(
        'SELECT user_name, user_surname, user_patronymic, '
        'user_phone, delivery_address, current_orders, '
        'completed_orders, canceled_orders FROM users WHERE '
        'user_telegram_id = $1;',
        user_telegram_id
    )

    await connection.close()

    return result[0]


async def select_user_pk(user_telegram_id: int) -> tuple:
    '''
    An async function to select user_pk from the users table
    :param user_telegram_id: user's telegram id
    '''
    database_data = get_database_data()
    connection = await asyncpg.connect(**database_data)

    result = await connection.fetch(
        'SELECT user_id FROM users WHERE user_telegram_id = $1;',
        user_telegram_id
    )

    await connection.close()

    return result[0]


async def increase_current_orders(user_telegram_id: int) -> None:
    '''
    An async function to increase current orders in the users table
    :param user_telegram_id: user's telegram id
    '''
    database_data = get_database_data()
    connection = await asyncpg.connect(**database_data)

    await connection.execute(
        'UPDATE users SET current_orders = current_orders + 1 '
        'WHERE user_telegram_id = $1;',
        user_telegram_id
    )

    await connection.close()


async def cancel_user_order(user_telegram_id: int) -> None:
    '''
    An async function to cancel user order in the users table
    :param user_telegram_id: user's telegram id
    '''
    database_data = get_database_data()
    connection = await asyncpg.connect(**database_data)

    await connection.execute(
        'UPDATE users SET current_orders = current_orders - 1,'
        'canceled_orders = canceled_orders + 1 '
        'WHERE user_telegram_id = $1;',
        user_telegram_id
    )

    await connection.close()
