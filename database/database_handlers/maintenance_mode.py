import asyncpg

from database.database_settings.database_data import get_database_data


async def get_maintenance_mode_value() -> bool:
    '''
    An async function to get the maintenance mode value
    '''
    database_data = get_database_data()
    connection = await asyncpg.connect(**database_data)

    result = await connection.fetchrow(
        'SELECT is_enabled FROM maintenance_mode;'
    )

    await connection.close()

    try:
        maintenance_mode_value = result[0]
    except TypeError:
        maintenance_mode_value = False

    return maintenance_mode_value


async def set_maintenance_mode_value(maintenance_mode_value: bool) -> None:
    '''
    An async function to set the maintenance mode value
    '''
    database_data = get_database_data()
    connection = await asyncpg.connect(**database_data)

    await connection.execute(
        'UPDATE maintenance_mode SET is_enabled = $1;',
        maintenance_mode_value

    )

    await connection.close()
