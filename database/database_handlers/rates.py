import asyncpg

from database.database_settings.database_data import get_database_data


async def get_course_and_commission() -> list:
    '''
    An async function to get the CNY course and service commission
    '''
    database_data = get_database_data()
    connection = await asyncpg.connect(**database_data)

    result = await connection.fetch(
        'SELECT rate_value, commission FROM rates '
        'WHERE rate_code = \'CNY\';'
    )

    await connection.close()

    try:
        rates_data = [data for data in result[0]]
    except IndexError:
        rates_data = ['Не указан курс', 'Не указана комиссия']

    return rates_data
