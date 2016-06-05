# -*- coding: utf-8 -*-
from mydynamodb.utils import add_product_price_item
import xlrd
import os

product_code = ('LP2', 'SG5', 'LB12', 'FY7', 'SO1', 'SH5', 'T1', 'R3', 'FB11', 'LD1', 'SE1', 'FT1', 'SD1',
                'A1', '45', 'SC1', 'LA1', 'FK4', 'C1', 'FJ3', 'LH1', 'S1', 'FV1', 'B2', 'X69', 'SA32', 'SA3', 'SA31')

def collect_data(rowx, product, region):
    date = sheet.cell(rowx, 0).value
    price = sheet.cell(rowx, 6).value
    turnover = sheet.cell(rowx, 8).value
    # change date format from yy.mm.dd to yy-mm-dd
    date = date.replace('/', '-')
    ad_year = int(date[:3]) + 1911
    ad_date = str(ad_year) + date[3:]
    add_product_price_item(product, ad_date, region, price, turnover)

dirs = os.listdir('veggg')
for filename in dirs:
    product = filename[:-4]
    print('Retrieving data: ', filename)

    workbook = xlrd.open_workbook('veggg/' + filename)
    sheet = workbook.sheet_by_name('Sheet1')

    markets = sheet.col(1)
    for i, market in enumerate(markets):
        name = market.value.split(' ')[0]
        product_code = sheet.cell(i, 2).value.split(' ')[0]
        if  product_code in product_code:
            if '260' == name:
                collect_data(i, product, 'YILAN')
            #elif '338' == namee:
                #collect_data(i, product, 'TAOYUAN')
            elif '400' == name:
                collect_data(i, product, 'TAICHUNG')
            elif '800' == name:
                collect_data(i, product, 'KAOHSIUNG')
            elif '930' == name:
                collect_data(i, product, 'TAITUNG')

