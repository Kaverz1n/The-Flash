import os


def get_database_data() -> dict:
    '''
    A function to get the database data
    '''
    database_data = {
        'database': os.getenv('DATABASE_NAME'),
        'user': os.getenv('DATABASE_USERNAME'),
        'password': os.getenv('DATABASE_PASSWORD'),
        'host': os.getenv('DATABASE_HOST'),
        'port': os.getenv('DATABASE_PORT')
    }

    return database_data
