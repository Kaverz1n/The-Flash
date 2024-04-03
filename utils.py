import os

from cdek.api import CDEKClient


async def is_correct_address(city_post_code: str, delivery_address: str) -> bool:
    '''
    An async function to check if the delivery address is correct
    :param city_post_code: city's post code
    :param delivery_address: delivery address
    :return: bool
    '''
    is_corrected = False

    try:
        cdek_client = CDEKClient(os.getenv('CDEK_LOGIN'), os.getenv('CDEK_PASSWORD'))
        delivery_points = cdek_client.get_delivery_points(city_post_code=city_post_code)['pvz']

        for delivery_point in delivery_points:
            cdek_address = ', '.join(delivery_point['fullAddress'].split(', ')[:6])

            if all(part in cdek_address for part in delivery_address.split(', ')):
                is_corrected = True
    finally:
        return is_corrected
