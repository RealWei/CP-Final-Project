#coding=utf-8

from mydynamodb.utils import *
import csv

datas = retieve_training_data('WATERMELON','KAOHSIUNG', '2007-01-01', '2015-12-31')
'''
for dd in datas:
    for key, value in dd.items() :
        if type(value) is list:
            print (key,len(value),'\n', value)
        else:
            print(key,'\n',value)
    print('\n\n')
'''
WEATHER_HOSTORY_SIZE = 30
TRADING_DATA_HISTORY_SIZE = 5
fieldnames =[]
for i in range(WEATHER_HOSTORY_SIZE):
    fieldnames.append('temperature_'+str(i))
for i in range(WEATHER_HOSTORY_SIZE):
    fieldnames.append('rainfall_'+str(i))
for i in range(WEATHER_HOSTORY_SIZE):
    fieldnames.append('humidity_'+str(i))

for i in range(TRADING_DATA_HISTORY_SIZE):
    fieldnames.append('price_'+str(i))
for i in range(TRADING_DATA_HISTORY_SIZE):
    fieldnames.append('turnover_'+str(i))

fieldnames += ['month', 'today_temperature', 'today_rainfall', 'today_humidity', 'today_price']
print(len(fieldnames))

with open('input.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)

    writer.writerow(fieldnames)
    for row in datas:
        writer.writerow(row['temperature'][0:-1] + row['rainfall'][0:-1] + row['humidity'][0:-1] + row['price'] + row['turnover'] + [row['month'], row['temperature'][-1], row['rainfall'][-1], row['humidity'][-1], row['ground_truth']] )

