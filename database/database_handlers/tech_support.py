import asyncpg

from database.database_settings.database_data import get_database_data


async def get_tech_support_information() -> list:
    '''
    An async function to get tech support data
    '''
    database_data = get_database_data()
    connection = await asyncpg.connect(**database_data)

    result = await connection.fetch(
        'SELECT * FROM tech_support;'
    )

    await connection.close()

    return result


async def get_tech_support_nicknames() -> list:
    '''
    An async function to get tech support nicknames
    '''
    database_data = get_database_data()
    connection = await asyncpg.connect(**database_data)

    result = await connection.fetch(
        'SELECT tech_support_telegram_nickname FROM tech_support;'
    )

    tech_support_nicknames = [tech_support_nickname[0] for tech_support_nickname in result]

    await connection.close()

    return tech_support_nicknames


async def insert_tech_support_data(tech_support_nickname: str) -> None:
    '''
    An async function to insert tech support data into the tech_support table
    :param tech_support_nickname: tech support's nickname
    '''
    database_data = get_database_data()
    connection = await asyncpg.connect(**database_data)

    await connection.execute(
        'INSERT INTO tech_support (tech_support_telegram_nickname) VALUES ($1)',
        tech_support_nickname
    )

    await connection.close()


async def delete_from_tech_support(tech_support_nickname: str) -> None:
    '''
    An async function to delete tech support data from the tech_support table
    :param tech_support_nickname: tech support's nickname
    '''
    database_data = get_database_data()
    connection = await asyncpg.connect(**database_data)

    await connection.execute(
        'DELETE FROM  tech_support WHERE tech_support_telegram_nickname = $1',
        tech_support_nickname
    )

    await connection.close()
