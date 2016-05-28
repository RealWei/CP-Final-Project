from __future__ import print_function # Python 2/3 compatibility
from mydynamodb.setting import dynamodb_resource, dynamodb_client, WEATHER_TABLE, PRODOCT_PRICE_TABLE
from mydynamodb.attribute_key import *
import boto3

existing_table_names = dynamodb_client.list_tables()['TableNames']
if WEATHER_TABLE in existing_table_names:
    print('{} Table is already exists'.format(WEATHER_TABLE))
else:
    weather_table = dynamodb_resource.create_table(
        TableName=WEATHER_TABLE,
        KeySchema=[
            {
                'AttributeName': key_region,
                'KeyType': 'HASH'  #Partition key
            },
            {
                'AttributeName': key_date,
                'KeyType': 'SORT'  #Partition key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': key_region,
                'AttributeType': 'S'
            },
            {
                'AttributeName': key_date,
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

    print("Weather Table status:", weather_table.table_status)

if PRODOCT_PRICE_TABLE in existing_table_names:
    print('{} Table is already exists'.format(PRODOCT_PRICE_TABLE))
else:
    prodoct_price_table = dynamodb_resource.create_table(
        TableName=PRODOCT_PRICE_TABLE,
        KeySchema=[
            {
                'AttributeName': key_product,
                'KeyType': 'HASH'  #Partition key
            },
            {
                'AttributeName': key_date,
                'KeyType': 'SORT'  #Partition key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': key_product,
                'AttributeType': 'S'
            },
            {
                'AttributeName': key_date,
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

    print("Prodoct Price Table status:", prodoct_price_table.table_status)