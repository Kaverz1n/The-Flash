import asyncpg

from database.database_settings.database_data import get_database_data


async def get_rate_and_commission() -> list:
    '''
    An async function to get the CNY rate and service commission
    '''
    database_data = get_database_data()
    connection = await asyncpg.connect(**database_data)

    result = await connection.fetch(
        'SELECT rate_value, commission FROM rates '
        'WHERE rate_code = \'CNY\';'
    )

    await connection.close()

    try:
        rates_data = [round(data, 2) for data in result[0]]
    except IndexError:
        rates_data = ['Не указан курс', 'Не указана комиссия']

    return rates_data


async def update_rate(rate_value: float) -> None:
    '''
    An async function to update the CNY rate
    :param rate_value: CNY rate
    '''
    database_data = get_database_data()
    connection = await asyncpg.connect(**database_data)

    await connection.execute(
        'UPDATE rates SET rate_value = $1 WHERE rate_code = \'CNY\'',
        rate_value
    )

    await connection.close()


async def update_commission(commission: float) -> None:
    '''
    An async function to update the service commission
    :param commission: service commission value
    '''
    database_data = get_database_data()
    connection = await asyncpg.connect(**database_data)

    await connection.execute(
        'UPDATE rates SET commission = $1 WHERE rate_code = \'CNY\'',
        commission
    )

    await connection.close()
