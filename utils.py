import os

from cdek.api import CDEKClient

from openpyxl import Workbook
from openpyxl.styles import Font


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


async def create_inf_file(data_list: list, headers: list) -> None:
    '''
    An async function to create an excel file with data
    :param data_list: a list with data
    :param headers: names of the columns
    '''
    with open(f'templates/excel_template.xlsx', 'w', encoding='UTF-8'):
        workbook = Workbook()
        sheet = workbook.active

        bold_font = Font(bold=True)
        for column_num, header in enumerate(headers, start=1):
            cell = sheet.cell(row=1, column=column_num)
            cell.value = header
            cell.font = bold_font

        for data in data_list:
            data_elements = [data_element for data_element in data]
            sheet.append(data_elements)

            workbook.save('templates/data.xlsx')
            workbook.close()
