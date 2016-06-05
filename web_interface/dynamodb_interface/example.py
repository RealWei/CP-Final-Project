#coding=utf-8

from mydynamodb.utils import add_weather_item, add_product_price_item, get_poduct_price_record
from mydynamodb.attribute_checker import valid_products, valid_regions

# Add Product Price Example
product = 'SPINACH'
date = '2016-06-05'
trading_datas = [
    {
        'region':'TAOYUAN',
        'price': 50,
        'turnover': 123
    },
    {
        'region':'YILAN',
        'price': 33,
        'turnover': 10.0
    },
    {
        'region':'TAICHUNG',
        'price': 54,
        'turnover': 87
    },
    {
        'region':'KAOHSIUNG',
        'price': 12.5,
        'turnover': 33.5
    },
    {
        'region':'TAITUNG',
        'price': 0.12,
        'turnover': 2E2
    }
]
'''
add_product_price_item(product, date, trading_datas)

# Add Weather Record Example
region = 'YILAN'
date = '2016-04-01'
temperature = 42
rainfall = 94.87
humidity = 66.66    # valid value is 0 ~ 100
add_weather_item(region, date, temperature, rainfall, humidity)

# Reteive Product Histrical Price
# There are only 2 sample product price records in database now
data = get_poduct_price_record('PONKAN', 'TAICHUNG')
print(data['product'])
print(data['region'])
print(data['starting_date'])    # will be an empty string if the list of price is empty
print(data['ending_date'])      # will be an empty string if the list of price is empty
print(data['price'])            # list of price

data = get_poduct_price_record('CABBAGE', 'KAOHSIUNG')
print(data['product'])
print(data['region'])
print(data['starting_date'])    # will be an empty string if the list of price is empty
print(data['ending_date'])      # will be an empty string if the list of price is empty
print(data['price'])            # list of price
'''
for product in valid_products:
    for region in valid_regions:
        data = get_poduct_price_record(product, region)
        print('{} @ {}'.format(data['product'],data['region']))
        print('{} ~ {}'.format(data['starting_date'],data['ending_date']))
        print(data['price'])            # list of price