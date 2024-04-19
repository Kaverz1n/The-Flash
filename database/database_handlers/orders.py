import asyncpg

from database.database_settings.database_data import get_database_data


async def get_order_status(order_status_name: str) -> int:
    '''
    An async function to get order status id
    :param order_status_name: status name
    '''
    database_data = get_database_data()
    connection = await asyncpg.connect(**database_data)

    result = await connection.fetch(
        'SELECT order_status_id FROM order_statuses '
        'WHERE order_status_name = $1',
        order_status_name
    )

    await connection.close()

    order_status_id = result[0][0]

    return order_status_id


async def insert_order_data(
        order_url: str, yuan_price: int, rub_price: int,
        order_photo_id: str, order_size: str, user_id: int,
        chat_telegram_id: int
) -> None:
    '''
    An async function to insert order data into the orders table
    :param order_url: order's url
    :param yuan_price: order's yuan price
    :param rub_price: order's rub price
    :param order_photo_id: order's photo id
    :param order_size: order's size
    :param user_id: order's user id
    :param chat_telegram_id: chat telegram id with customer
    '''
    database_data = get_database_data()
    connection = await asyncpg.connect(**database_data)

    order_status = await get_order_status('Создан')

    await connection.execute(
        'INSERT INTO orders (order_url, yuan_price, rub_price, '
        'order_photo_id, order_size, user_id, chat_telegram_id, order_status_id) '
        'VALUES ($1, $2, $3, $4, $5, $6, $7, $8)',
        order_url, yuan_price, rub_price, order_photo_id,
        order_size, user_id, chat_telegram_id, order_status
    )

    await connection.close()


async def get_orders_inf() -> list:
    '''
    An async function to get orders data
    '''
    database_data = get_database_data()
    connection = await asyncpg.connect(**database_data)

    result = await connection.fetch(
        'SELECT o.order_id, o.order_url, o.yuan_price, o.rub_price, o.order_photo_id, '
        'o.order_size, u.user_telegram_id, o.chat_telegram_id, os.order_status_name '
        'FROM orders o '
        'JOIN order_statuses os ON o.order_status_id = os.order_status_id '
        'JOIN users u ON o.user_id = u.user_id '
        'ORDER BY CASE WHEN os.order_status_name = \'Создан\' THEN 0 ELSE 1 END, os.order_status_name'
    )

    await connection.close()

    return result


async def get_order_inf(order_id: int) -> list:
    '''
    An async function to get one order data
    :param order_id: order id
    '''
    database_data = get_database_data()
    connection = await asyncpg.connect(**database_data)

    result = await connection.fetch(
        'SELECT o.order_id, o.order_url, o.yuan_price, o.rub_price, o.order_photo_id, '
        'o.order_size, u.user_telegram_id, o.chat_telegram_id, os.order_status_name '
        'FROM orders o '
        'JOIN order_statuses os ON o.order_status_id = os.order_status_id '
        'JOIN users u ON o.user_id = u.user_id '
        'WHERE order_id = $1',
        order_id
    )

    await connection.close()

    return result[0]


async def update_order_status(order_id: int, status_name: str) -> None:
    '''
    An async function to update order status
    :param order_id: order id
    :param status_name: status name
    '''
    database_data = get_database_data()
    connection = await asyncpg.connect(**database_data)

    order_status = await get_order_status(status_name)

    await connection.execute(
        'UPDATE orders SET order_status_id = $1 '
        'WHERE order_id = $2',
        order_status, order_id
    )

    await connection.close()

