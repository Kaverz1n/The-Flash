import asyncpg

from database.database_settings.database_data import get_database_data


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

    await connection.execute(
        'INSERT INTO orders (order_url, yuan_price, rub_price, '
        'order_photo_id, order_size, user_id, chat_telegram_id) '
        'VALUES ($1, $2, $3, $4, $5, $6, $7)',
        order_url, yuan_price, rub_price, order_photo_id,
        order_size, user_id, chat_telegram_id
    )

    await connection.close()
