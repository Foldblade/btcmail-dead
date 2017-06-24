# encoding:utf-8

import datetime
import pandas
import csv
import urllib.request
import linecache
import json
import requests
import os

where_script = os.path.split(os.path.realpath(__file__))[0]

now = datetime.datetime.now()
now.strftime('%Y-%m-%d %H:%M:%S')
nowtime = now.strftime('%Y-%m-%d %H:%M:%S')
print(nowtime)

coins = ['btc', 'eth', 'ltc', 'doge', 'ybc']

f = open(where_script + '/data/pricenow.json', 'r')
pricedata = json.load(f)
f.close()
pricedata['time'] = nowtime
# 用来存储获得的当前价格，参考json文件吧。
# 当前价格coin + last、上一次价格coin + previous、当前买一价coin + buy、当前卖一价coin + sell、上一买一价coin + pre_buy、上一卖一价coin + pre_sell、当前交易量coin + vol 、上一交易量coin + pre_vol
# 下面两个函数用来填充pricedata


def previous(coin):
    data = pandas.read_csv(where_script + '/data/pricelog_min.csv')
    finlinedata = data.iloc[-1, ]
    # print(finlinedata)
    # print(float(finlinedata[coin]))
    # print(float(finlinedata[coin + '_buy']))
    # print(float(finlinedata[coin + '_sell']))
    pricedata[str(coin)]['previous'] = float(finlinedata[coin])
    pricedata[str(coin)]['pre_buy'] = float(finlinedata[coin + '_buy'])
    pricedata[str(coin)]['pre_sell'] = float(finlinedata[coin + '_sell'])
    pricedata[str(coin)]['pre_vol'] = int(finlinedata[coin + '_vol'])
    return pricedata


def priceget(coin):
    try:
        url = 'https://api.btctrade.com/api/ticker?coin=' + str(coin)
        response = requests.get(url, timeout=5).text
        # 抓取比特币价格网页
        js_dict = json.loads(response)
        print(coin + str(js_dict['last']))
        print(coin + 'sell:' + str(js_dict['sell']))
        print(coin + 'buy:' + str(js_dict['buy']))
        pricedata[str(coin)]['price'] = js_dict['last']
        pricedata[str(coin)]['buy'] = js_dict['buy']
        pricedata[str(coin)]['sell'] = js_dict['sell']
        pricedata[str(coin)]['vol'] = js_dict['vol']
        pricedata[str(coin)]['trend'] = round(pricedata[str(coin)]['price'] - pricedata[str(coin)]['previous'], 5)
        return pricedata
    except:
        pricedata[str(coin)]['price'] = pricedata[str(coin)]['previous']
        pricedata[str(coin)]['buy'] = pricedata[str(coin)]['pre_buy']
        pricedata[str(coin)]['sell'] = pricedata[str(coin)]['pre_sell']
        pricedata[str(coin)]['sell'] = pricedata[str(coin)]['pre_vol']
        pricedata[str(coin)]['trend'] = round(pricedata[str(coin)]['price'] - pricedata[str(coin)]['previous'], 5)
        return pricedata

for coin in coins:
    previous(coin)
    priceget(coin)

data = pandas.read_csv(where_script + '/data/pricelog_min.csv')
data = data.drop(0)
data.to_csv(where_script + '/data/pricelog_min.csv', sep=",", index=False)
#删价格首行

f = open(where_script + '/data/pricelog_min.csv','a+')
data = nowtime
for coin in coins:
    data = data + ',' + str(pricedata[coin]['price']) + ',' + str(pricedata[coin]['trend']) +  ',' + str(pricedata[coin]['buy']) + ',' + str(pricedata[coin]['sell']) + ',' + str(pricedata[coin]['vol'])
f.write(data)
f.close()
#记录价格


f = open(where_script + '/data/pricenow.json', 'w')
json.dump(pricedata, f, indent=4)
f.close()

print('record done!')

import analyse.py
