from .chinese_name import *
import re

valid_regions = (TAOYUAN, YILAN, TAICHUNG, KAOHSIUNG, TAITUNG)
valid_products = (
    BASIL, GARLIC, BOK_CHOY, CORN, SWEET_POTATO,
    BAMBOO_SHOOT, WATERMELON, MANGO, BROCCOLI, SPOON_CABBAGE,
    SHALLOT, BANANA, POTATO, CABBAGE, SWEET_PEPPER,
    PONKAN, TOMATO, SPINACH, GRAPE, CHILI,
    PINEAPPLE, APPLE, RADISH, PUMPKIN, ONION,
    STRAWBERRY
)
date_validator = re.compile('^[0-9]{4}-[0-9]{2}-[0-9]{2}$')

def check_region(region):
    if not region in valid_regions:
        raise Exception('{} is not a valid "region" attribute'.format(region))

def check_date(date):
    if not date_validator.match(date):
        raise Exception('{} is not a valid "date" attribute'.format(date))

def check_rainfall(rainfall):
    if not rainfall >= 0:
        raise Exception('value of "rainfall" attribute must >= 0')

def check_humidity(humidity):
    if not (humidity >= 0 and humidity <= 100):
        raise Exception('value of "humidity" attribute must >= 0 and <= 100')

def check_product(product):
    if not product in valid_products:
        raise Exception('{} is not a valid "product" attribute'.format(product))

def check_price(price):
    if not price >= 0:
        raise Exception('value of "price" attribute must >= 0')

def check_turnover(turnover):
    if not turnover >= 0:
        raise Exception('value of "turnover" attribute must >= 0')