# -*- coding: utf-8 -*-
from mydynamodb.utils import add_weather_item
import random
import xml.etree.ElementTree as ET


ns = {'d': 'urn:cwb:gov:tw:cwbcommon:0.1'}
TY_data = {'temperature': {}, 'humidity': {}}
YL_data = {'temperature': {}, 'humidity': {}}
TC_data = {'temperature': {}, 'humidity': {}}
KS_data = {'temperature': {}, 'humidity': {}}
TT_data = {'temperature': {}, 'humidity': {}}


def get_temperature_and_humidity(location):

    elements = location.findall('d:weatherElement', ns)
    for element in elements:
        name = element.find('d:elementName', ns).text
        if name == '平均溫度':
            temperature = element.find('d:elementValue', ns).find('d:value', ns).text
        if name == '平均相對濕度':
            humidity = element.find('d:elementValue', ns).find('d:value', ns).text
    return temperature, humidity

def get_inter_value(region, year_month):
    if region == 'YILAN':
        this_month_temperature = YL_data['temperature'][year_month]
        this_month_humidity = YL_data['humidity'][year_month]
        if(year_month[-2:] == 12): year_month = str(int(year_month[:4])+1) + '-01'
        next_month_temperature = YL_data['temperature'][year_month]
        next_month_humidity = YL_data['humidity'][year_month]
        T = (next_month_temperature - this_month_temperature)/30.0
        H = (next_month_humidity - this_month_humidity)/30.0
    elif region == 'TAICHUNG':
        this_month_temperature = TC_data['temperature'][year_month]
        this_month_humidity = TC_data['humidity'][year_month]
        if(year_month[-2:] == 12): year_month = str(int(year_month[:4])+1) + '-01'
        next_month_temperature = TC_data['temperature'][year_month]
        next_month_humidity = TC_data['humidity'][year_month]
        T = (next_month_temperature - this_month_temperature)/30.0
        H = (next_month_humidity - this_month_humidity)/30.0
    elif region == 'KAOHSIUNG':
        this_month_temperature = KS_data['temperature'][year_month]
        this_month_humidity = KS_data['humidity'][year_month]
        if(year_month[-2:] == 12): year_month = str(int(year_month[:4])+1) + '-01'
        next_month_temperature = KS_data['temperature'][year_month]
        next_month_humidity = KS_data['humidity'][year_month]
        T = (next_month_temperature - this_month_temperature)/30.0
        H = (next_month_humidity - this_month_humidity)/30.0
    elif region == 'TAITUNG':
        this_month_temperature = TT_data['temperature'][year_month]
        this_month_humidity = TT_data['humidity'][year_month]
        if(year_month[-2:] == 12): year_month = str(int(year_month[:4])+1) + '-01'
        next_month_temperature = TT_data['temperature'][year_month]
        next_month_humidity = TT_data['humidity'][year_month]
        T = (next_month_temperature - this_month_temperature)/30.0
        H = (next_month_humidity - this_month_humidity)/30.0

    return this_month_temperature, this_month_humidity, T, H

def collect_data(location, region):
    days = location.find('d:weatherElement', ns).findall('d:time', ns)
    for day in days:
        date = day.find('d:dataTime', ns).text
        year_month = date[:7]
        d = date[8:]

        if(d == '01'):
            this_month_T, this_month_H, inter_value_T, inter_value_H = get_inter_value(region, year_month)

        temperature = this_month_T + (float(d)-1)*inter_value_T + random.uniform(0, 1)
        humidity = this_month_H + (float(d)-1)*inter_value_H + random.uniform(0, 1)
        rainfall = day.find('d:elementValue', ns).find('d:value', ns).text
        # 原始資料缺漏
        if rainfall == 'T': rainfall = 0
        print (date, region)
        add_weather_item(region, date, temperature, rainfall, humidity)


for year in range(2007, 2016, 1):

    # 每月氣象-過去9年局屬地面測站每月氣象資料
    filename = 'C-B0026-002/mn_Report_' + str(year) + '.xml'
    root = ET.parse(filename).getroot()

    months = root.find('d:dataset', ns).findall('d:time', ns)
    for month in months:
        date = month.find('d:dataTime', ns).text
        locations = month.findall('d:location', ns)
        for location in locations:
            name = location.find('d:locationName', ns).text
            #if name == 'XINWU,新屋':
                #get_temperature_and_humidity(location, date, 'TAOYUAN')
            if name == 'YILAN,宜蘭':
                temperature, humidity = get_temperature_and_humidity(location)
                YL_data['temperature'][date] = float(temperature)
                YL_data['humidity'][date] = float(humidity)
            if name == 'TAICHUNG,臺中':
                temperature, humidity = get_temperature_and_humidity(location)
                TC_data['temperature'][date] = float(temperature)
                TC_data['humidity'][date] = float(humidity)
            if name == 'KAOHSIUNG,高雄':
                temperature, humidity = get_temperature_and_humidity(location)
                KS_data['temperature'][date] = float(temperature)
                KS_data['humidity'][date] = float(humidity)
            if name == 'TAITUNG,臺東':
                temperature, humidity = get_temperature_and_humidity(location)
                TT_data['temperature'][date] = float(temperature)
                TT_data['humidity'][date] = float(humidity)

print("Monthly Weather Data From 2007~2015 Retrieved Successfully!")

for year in range(2007, 2016, 1):
    # 每日雨量-過去9年局屬地面測站每日雨量資料
    filename = 'C-B0025-002/dy_Report_' + str(year) + '.xml'
    print(filename)
    root = ET.parse(filename).getroot()

    locations = root.find('d:dataset', ns).findall('d:location', ns)
    for location in locations:
        name = location.find('d:locationName', ns).text
        #if name == 'XINWU,新屋': collect_data(location, 'TAOYUAN')
        if name == 'YILAN,宜蘭': collect_data(location, 'YILAN')
        if name == 'TAICHUNG,臺中': collect_data(location, 'TAICHUNG')
        if name == 'KAOHSIUNG,高雄': collect_data(location, 'KAOHSIUNG')
        if name == 'TAITUNG,臺東': collect_data(location, 'TAITUNG')


