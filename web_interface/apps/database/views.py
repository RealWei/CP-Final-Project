import json

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render

from dynamodb_interface.mydynamodb.utils import add_weather_item, add_product_price_item, get_poduct_price_record

def getData(request):
    product = request.GET.get('product', '高麗菜')
    location = request.GET.get('location', '高雄')
    data = get_poduct_price_record(product, location)
    response_data = json.dumps(data, ensure_ascii=False)
    response = HttpResponse(response_data, content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'POST, GET'
    response['Access-Control-Max-Age'] = '1000'
    response['Access-Control-Allow-Headers'] = '*'
    response['charset'] = 'utf-8'
    return response
