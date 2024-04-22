import asyncpg

from database.database_settings.database_data import get_database_data


async def get_admins_information() -> list:
    '''
    An async function to get admin data
    '''
    database_data = get_database_data()
    connection = await asyncpg.connect(**database_data)

    result = await connection.fetch(
        'SELECT * FROM admins;'
    )

    await connection.close()

    return result

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


async def insert_admin_data(admin_telegram_id: int, admin_password: str) -> None:
    '''
    An async function to insert admin data into the admins table
    :param admin_telegram_id: admin's telegram id
    :param admin_password: admin's password
    '''
    database_data = get_database_data()
    connection = await asyncpg.connect(**database_data)

    await connection.execute(
        'INSERT INTO admins (admin_telegram_id, admin_password) VALUES ($1, $2)',
        admin_telegram_id, admin_password
    )

    await connection.close()


async def delete_from_admins(admin_telegram_id: int) -> None:
    '''
    An async function to delete admin data from the admins table
    :param admin_telegram_id: admin's telegram id
    '''
    database_data = get_database_data()
    connection = await asyncpg.connect(**database_data)

    await connection.execute(
        'DELETE FROM admins WHERE admin_telegram_id = $1',
        admin_telegram_id
    )

    await connection.close()


async def select_admin_password(admin_telegram_id: int) -> None:
    '''
    An async function to select admin password
    :param admin_telegram_id: admin's telegram id
    '''
    database_data = get_database_data()
    connection = await asyncpg.connect(**database_data)

    result = await connection.fetch(
        'SELECT admin_password FROM admins'
        ' WHERE admin_telegram_id = $1',
        admin_telegram_id
    )

    admin_password = result[0][0]

    await connection.close()

    return admin_password
