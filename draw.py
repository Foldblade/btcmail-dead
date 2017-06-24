# encoding:utf-8
import os
import pandas
import csv
import matplotlib as mpl
import numpy
mpl.use('Agg')
import matplotlib.pyplot as plt
import datetime
from matplotlib.ticker import MultipleLocator
import matplotlib.dates as mdate
import os
import json

where_script = os.path.split(os.path.realpath(__file__))[0]

now = datetime.datetime.now()
now.strftime('%Y-%m-%d %H:%M')
nowtime = now.strftime('%Y-%m-%d %H:%M')
print(nowtime)

coins = ['btc', 'eth', 'ltc', 'doge', 'ybc']
f = open(where_script + '/setting.json', 'r')
setting = json.load(f)
f.close()
for coin in coins:
    if setting[coin]['draw'] == 0:
        coins.remove(coin)
    else :
        pass
# print(coins)

def  pricelog(coin):
    global date, pricelist, vollist, average, length

    with open("data/pricelog_min.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        date = [row['time'] for row in reader]
        # print(len(date))
        csvfile.close()

    with open("data/pricelog_min.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        pricelist = [row[ str(coin) ] for row in reader]
        # print(len(pricelist))
        csvfile.close()

    with open("data/pricelog_min.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        vollist = [row[ str(coin)+'_vol' ] for row in reader]
        # print(len(vollist))
        csvfile.close()

    f = open("data/pricelog_min.csv",'r')
    length = len(f.readlines())-1
    f.close()
    # print(length)

    sum = 0
    for obj in pricelist:
        sum = sum + float(obj)
    # print(sum)
    average = sum / length
    average = round(average, 3)
    print('average=', average)
    # 求平均值
    return date, pricelist, average


def draw(coin):
    fig = plt.figure(figsize=(21, 9), dpi=200)
    pricelog(coin)
    # xmajorLocator = MultipleLocator(1)
    ax1 = fig.add_subplot(111)
    ax1.xaxis.set_major_formatter(mdate.DateFormatter('%H:%M'))  # 设置时间标签显示格式
    plt.xticks(pandas.date_range(date[0], date[-1], freq='10min'))  # 时间间隔
    plt.xticks(rotation=90, fontsize=8)
    ax1.set_xlabel('Time (freq=10min)', size=15)
    ax1.set_ylabel('Price/¥', size=15)
    ax1.set_title(coin.upper() + ' Price Daily' + '\n' + nowtime, size=20)
    ax1.plot(date, pricelist, linewidth=1.0, label='Price')
    ax1.plot(date, [average for obj in date], linewidth=1.0, linestyle='-.',label='Average')
    ax1.legend(loc='upper left')
    ax1.grid(True)

    ax2 = ax1.twinx()
    ax2.xaxis.set_major_formatter(mdate.DateFormatter('%H:%M'))  # 设置时间标签显示格式
    plt.xticks(pandas.date_range(date[0], date[-1], freq='10min'))  # 时间间隔
    ax2.plot(date, vollist, linewidth=2.0, label='Vol', color='g', linestyle=':',alpha=0.8)
    #ax2.fill_between(date, vollist,y2=0, color='g', alpha=.25)
    #ax2.fill(date, vollist)
    #ax2.hist(range(length), vollist, normed=1, histtype='bar', rwidth=0.8)
    #ax2.stackplot(range(length), vollist)
    #ax2.bar(range(length), vollist)
    ax2.set_ylabel('Vol')
    ax2.legend(loc='upper right')
    # ax2.grid(True)
    plt.savefig(os.getcwd() + '/data/'+ coin + '.png', dpi=150)

    print('PNG saved!')
    return()

for coin in coins:
    draw(coin)