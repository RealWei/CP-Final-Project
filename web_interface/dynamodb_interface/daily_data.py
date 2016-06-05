# -*- coding: utf-8 -*-
from mydynamodb.utils import add_weather_item, add_product_price_item
import json
import urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as ET


product_code = ('LP2', 'SG5', 'LB12', 'FY7', 'SO1', 'SH5', 'T1', 'R3', 'FB11', 'LD1', 'SE1', 'FT1', 'SD1',
                'A1', '45', 'SC1', 'LA1', 'FK4', 'C1', 'FJ3', 'LH1', 'S1', 'FV1', 'B2', 'X69', 'SA32', 'SA3', 'SA31')

product_code_mapping = {'LP2':'BASIL', 'SG5':'GARLIC', 'LB12':'BOK_CHOY', 'FY7':'CORN', 'SO1':'SWEET_POTATO',
                    'SH5':'BAMBOO_SHOOT', 'T1':'WATERMELON', 'R3':'MANGO', 'FB11':'BROCCOLI', 'LD1':'SPOON_CABBAGE',
                    'SE1':'SHALLOT', 'FT1':'PUMPKIN', 'SD1':'ONION', 'A1':'BANANA', '45':'STRAWBERRY', 'SC1':'POTATO',
                    'LA1':'CABBAGE', 'FK4':'SWEET_PEPPER', 'C1':'PONKAN', 'FJ3':'TOMATO', 'LH1':'SPINACH', 'S1':'GRAPE',
                    'FV1':'CHILI', 'B2':'PINEAPPLE', 'X69':'APPLE', 'SA32':'RADISH', 'SA3':'RADISH', 'SA31':'RADISH'}



def marketFilter(market):

    flag = False
    if '宜蘭' in market:
        flag = True
        market = 'YILAN'
    elif '台中' in market:
        flag = True
        market = 'TAICHUNG'
    elif '高雄' in market:
        flag = True
        market = 'KAOHSIUNG'
    elif '台東' in market:
        flag = True
        market = 'TAITUNG'

    return flag, market

def collect_data(location, region):
    date = location.find('d:time', ns).find('d:obsTime', ns).text
    date = date[:10]
    elements = location.findall('d:weatherElement', ns)
    for element in elements:
        if element.find('d:elementName', ns).text == 'TEMP':
            temperature = float(element.find('d:elementValue', ns).find('d:value', ns).text)
            if temperature < -50:
                temperature = None
        if element.find('d:elementName', ns).text == 'H_24R':
            rainfall = float(element.find('d:elementValue', ns).find('d:value', ns).text)
            if rainfall < 0:
                rainfall = None
        if element.find('d:elementName', ns).text == 'HUMD':
            humidity = float(element.find('d:elementValue', ns).find('d:value', ns).text) * 100
            if humidity < 0:
                humidity = None

    add_weather_item(region, date, temperature, rainfall, humidity)


#農產品交易行情(每日更新)
url = "http://m.coa.gov.tw/OpenData/FarmTransData.aspx"

#type : string
data = urllib.request.urlopen(url).read()
print("Retrieved", len(data), "characters")
data = data.decode('utf-8')
info = json.loads(data)
for item in info:
    code = item['作物代號']
    product = item['作物名稱']
    date = item['交易日期']
    region = item['市場名稱']
    price = item['平均價']
    turnover = item['交易量']
    required_market, region = marketFilter(region)

    if  code in product_code and required_market:
        # change date format from yy.mm.dd to yy-mm-dd
        date = date.replace('.', '-')
        ad_year = int(date[:3]) + 1911
        ad_date = str(ad_year) + date[3:]
        add_product_price_item(product_code_mapping[code], ad_date, region, price, turnover)


# 自動氣象站-氣象觀測資料
url = 'http://opendata.cwb.gov.tw/opendataapi?dataid=O-A0001-001&authorizationkey=CWB-9A63F68D-76D1-4678-9514-8C5D82B7283B'
ns = {'d': 'urn:cwb:gov:tw:cwbcommon:0.1'}

root = ET.parse(urllib.request.urlopen(url)).getroot()

locations = root.findall('d:location', ns)

for location in locations:
    name = location.find('d:locationName', ns).text
    #if name == '桃園': collect_data(location, 'TAOYUAN')
    if name == '礁溪': collect_data(location, 'YILAN')
    if name == '大甲': collect_data(location, 'TAICHUNG')
    if name == '新興': collect_data(location, 'KAOHSIUNG')
    if name == '池上': collect_data(location, 'TAITUNG')

