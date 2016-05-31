#coding=utf-8
from __future__ import print_function
import boto3

REGION = 'us-west-2'
ENDPOINT = 'http://localhost:8000'
WEATHER_TABLE = 'Weather'
PRODOCT_PRICE_TABLE = 'ProductPrice'

dynamodb_resource = boto3.resource('dynamodb', region_name=REGION, endpoint_url=ENDPOINT)
dynamodb_client = boto3.client('dynamodb', region_name=REGION, endpoint_url=ENDPOINT)
weather_table = dynamodb_resource.Table(WEATHER_TABLE)
product_price_table = dynamodb_resource.Table(PRODOCT_PRICE_TABLE)
