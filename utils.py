import os

from cdek.api import CDEKClient
from openpyxl import Workbook
from openpyxl.styles import Font

from database.database_handlers.orders import get_orders_inf


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


async def create_order_inf_file() -> None:
    '''
    An async function to create an excel file with orders data
    '''
    orders_inf_list = await get_orders_inf()

    with open(f'templates/excel_template.xlsx', 'w', encoding='UTF-8') as excel_file:
        workbook = Workbook()
        sheet = workbook.active

        headers = [
            'id заказа', 'ссылка', 'цена в юан.', 'цена в руб.', 'id фото', 'размер',
            'telegram-id заказчика', 'telegram-id чата с заказчиком', 'статус заказа'
        ]

        bold_font = Font(bold=True)
        for column_num, header in enumerate(headers, start=1):
            cell = sheet.cell(row=1, column=column_num)
            cell.value = header
            cell.font = bold_font

        for order_inf in orders_inf_list:
            sheet.append([
                order_inf[0], order_inf[1], order_inf[2], order_inf[3], order_inf[4],
                order_inf[5], order_inf[6], order_inf[7], order_inf[8]
            ])

            workbook.save('templates/excel_template.xlsx')
            workbook.close()

