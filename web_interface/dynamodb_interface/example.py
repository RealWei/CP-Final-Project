#coding=utf-8
from __future__ import print_function
from mydynamodb.utils import add_weather_item, add_product_price_item, get_poduct_price_record

# Add Product Price Example
product = '菠菜'
date = '2016-06-05'
trading_datas = [
    {
        'region':'桃園',
        'price': 50,
        'turnover': 123
    },
    {
        'region':'宜蘭',
        'price': 33,
        'turnover': 10.0
    },
    {
        'region':'台中',
        'price': 54,
        'turnover': 87
    },
    {
        'region':'高雄',
        'price': 12.5,
        'turnover': 33.5
    },
    {
        'region':'台東',
        'price': 0.12,
        'turnover': 2E2
    }
]
add_product_price_item(product, date, trading_datas)

# Add Weather Record Example
region = '宜蘭'
date = '2016-04-01'
temperature = 42
rainfall = 94.87
humidity = 66.66    # valid value is 0 ~ 100
add_weather_item(region, date, temperature, rainfall, humidity)

# Reteive Product Histrical Price
# There are only 2 sample product price records in database now
data = get_poduct_price_record('椪柑', '台中')
print(data['product'])
print(data['region'])
print(data['starting_date'])    # will be an empty string if the list of price is empty
print(data['ending_date'])      # will be an empty string if the list of price is empty
print(data['price'])            # list of price

data = get_poduct_price_record('高麗菜', '高雄')
print(data['product'])
print(data['region'])
print(data['starting_date'])    # will be an empty string if the list of price is empty
print(data['ending_date'])      # will be an empty string if the list of price is empty
print(data['price'])            # list of price