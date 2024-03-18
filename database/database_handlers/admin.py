import asyncpg

from database.database_settings.database_data import get_database_data


async def get_admins_telegram_ids() -> list:
    '''
    An async function to get the list of admins' telegram_ids
    '''
    database_data = get_database_data()
    connection = await asyncpg.connect(**database_data)

    result = await connection.fetch(
        'SELECT admin_telegram_id FROM admins;'
    )

    await connection.close()

    admins_telegram_ids = [admin_telegram_id[0] for admin_telegram_id in result]

    return admins_telegram_ids
