from __future__ import print_function # Python 2/3 compatibility
from decimal import Decimal
from boto3.dynamodb.conditions import Key
from datetime import datetime, timedelta
from .chinese_name import *
from .attribute_checker import *
from .attribute_key import *
from .setting import weather_table, product_price_table

def add_weather_item(region, date, temperature, rainfall, humidity, overwrite = True):
    temperature =  Decimal(str(temperature))
    rainfall =  Decimal(str(rainfall))
    humidity =  Decimal(str(humidity))

    check_region(region)
    check_date(date)
    check_rainfall(rainfall)
    check_humidity(humidity)

    item_context = {
        key_date : date,
        key_region : region,
        key_temperature : temperature,
        key_rainfall : rainfall,
        key_humidity : humidity
    }
    if overwrite:
        weather_table.put_item(
            Item=item_context,
        )
    else:
        weather_table.put_item(
            Item=item_context,
            ConditionExpression='attribute_not_exists(#r) and attribute_not_exists(#d)',
            ExpressionAttributeNames={
                '#r':key_region,
                '#d':key_date
            }
        )

def add_product_price_item(product, date, trading_datas, overwrite = True):

    check_date(date)
    check_product(product)

    trading_datas_list={}
    for trading_data in trading_datas:
        region = trading_data[key_region]
        price = Decimal(str(trading_data[key_price]))
        turnover = Decimal(str(trading_data[key_turnover]))

        check_region(region)
        check_price(price)
        check_turnover(turnover)

        trading_datas_list[get_region_key(region)] = {
            key_price:price,
            key_turnover:turnover,
        }

    item_context = {
        key_product:product,
        key_date: date,
        key_trading_data: trading_datas_list
    }

    if overwrite:
        product_price_table.put_item(
            Item=item_context,
        )
    else:
        product_price_table.put_item(
            Item=item_context,
            ConditionExpression='attribute_not_exists(#p) and attribute_not_exists(#d)',
            ExpressionAttributeNames={
                '#p':key_product,
                '#d':key_date
            }
        )

def get_poduct_price_record(product, region, delta_starting_days=-90):
    check_product(product)
    check_region(region)

    response = product_price_table.query(
        ProjectionExpression='product, #d, trading_data.{}.price'.format(get_region_key(region)),
        ExpressionAttributeNames={'#d' : key_date },
        KeyConditionExpression=Key(key_product).eq(product) & Key(key_date).gte(get_starting_date(delta_starting_days))
    )
    return parse_product_prict_query_output(response['Items'], product, region)

def parse_product_prict_query_output(responseItem, product, region):
    __one_day_timedelta = timedelta(1)
    starting_date = ''
    previous_date = None
    if len(responseItem) > 0:
        ending_date = responseItem[-1][key_date]
    else:
        ending_date = ''
    price=[]
    region_key = get_region_key(region)
    for data in responseItem:
        # fix missing date price
        while previous_date and parse_string_to_date(data[key_date]) - previous_date > __one_day_timedelta:
            price.append(0.0)
            previous_date += __one_day_timedelta

        # fix missing region price
        if not key_trading_data in data:
            if starting_date == '':
                continue
            else:
                price.append(0.0)
                previous_date += __one_day_timedelta
        else:
            if starting_date == '':
                starting_date = data[key_date]
                previous_date = parse_string_to_date(starting_date)
            else:
                previous_date += __one_day_timedelta
            price.append(float(data[key_trading_data][region_key][key_price]))

    return {
        'product':product.decode('utf-8'),
        'region':region.decode('utf-8'),
        'starting_date':starting_date.decode('utf-8'),
        'ending_date':ending_date.decode('utf-8'),
        'price':price,
    }

def parse_string_to_date(date_string):
    return datetime.strptime(date_string, '%Y-%m-%d').date()

def get_region_key(region):
    if not region in valid_regions:
        raise Exception('{} is not a valid "region" attribute'.format(region))
    if region == TAOYUAN:
        return key_taoyuan
    elif region == YILAN:
        return key_yilan
    elif region == TAICHUNG:
        return key_taichung
    elif region == KAOHSIUNG:
        return key_kaohsiung
    elif region == TAITUNG:
        return key_taitung

def get_starting_date(delta_days):
    return str(datetime.now().date() + timedelta(delta_days))