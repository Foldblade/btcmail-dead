# encoding:utf-8
import os
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import datetime
from matplotlib.ticker import  MultipleLocator
import matplotlib.dates as mdate
import pandas
import csv

now = datetime.datetime.now()
now.strftime('%Y-%m-%d %H:%M')
nowtime = now.strftime('%Y-%m-%d %H:%M')
print(nowtime)

def  pricelog(name):
    global x, date, y, pricelist, average
    with open("data/pricelog-min.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        date = [row['time'] for row in reader]
        csvfile.close()
    x = date
    with open("data/pricelog-min.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        pricelist = [row[ name ] for row in reader]
        csvfile.close()
    y = pricelist

    sum = 0
    for obj in pricelist:
        sum = sum + float(obj)
    # print(sum)
    average = sum / 1440
    average = round(average, 3)
    print('average=', average)
    # 求平均值
    return(x, date, y, pricelist, average)


'''
fig=plt.figure(figsize=(36,9),dpi=200)


pricelog('btc')
xmajorLocator = MultipleLocator(1)
ax1=fig.add_subplot(131)
ax1.xaxis.set_major_formatter(mdate.DateFormatter('%H:%M'))#设置时间标签显示格式
plt.xticks(pandas.date_range(date[0],date[-1],freq='60min'))#时间间隔
plt.xticks(rotation=90)
plt.xticks(fontsize = 10)
ax1.set_xlabel('Time', size=15)
ax1.set_ylabel('Price/¥', size=15)
ax1.set_title('BTC Price Daily'+'\n'+ nowtime, size=20)
ax1.plot(x,y,linewidth=1.0,label='price')
ax1.plot(x,[average for obj in x],linewidth=1.0,label='average')
ax1.legend(loc='upper right')
ax1.grid(True)

pricelog('eth')
xmajorLocator = MultipleLocator(1)
ax2=fig.add_subplot(132)
ax2.xaxis.set_major_formatter(mdate.DateFormatter('%H:%M'))#设置时间标签显示格式
plt.xticks(pandas.date_range(date[0],date[-1],freq='60min'))#时间间隔
plt.xticks(rotation=90)
plt.xticks(fontsize = 10)
ax2.set_xlabel('Time', size=15)
ax2.set_ylabel('Price/¥', size=15)
ax2.set_title('ETH Price Daily'+'\n'+ nowtime, size=20)
ax2.plot(x,y,linewidth=1.0,label='price')
ax2.plot(x,[average for obj in x],linewidth=1.0,label='average')
ax2.legend(loc='upper right')
ax2.grid(True)

pricelog('ltc')
xmajorLocator = MultipleLocator(1)
ax3=fig.add_subplot(133)
ax3.xaxis.set_major_formatter(mdate.DateFormatter('%H:%M'))#设置时间标签显示格式
plt.xticks(pandas.date_range(date[0],date[-1],freq='60min'))#时间间隔
plt.xticks(rotation=90)
plt.xticks(fontsize = 10)
ax3.set_xlabel('Time', size=15)
ax3.set_ylabel('Price/¥', size=15)
ax3.set_title('LTC Price Daily'+'\n'+ nowtime, size=20)
ax3.plot(x,y,linewidth=1.0,label='price')
ax3.plot(x,[average for obj in x],linewidth=1.0,label='average')
ax3.legend(loc='upper right')
ax3.grid(True)


plt.savefig(os.getcwd() + "/data/pricepicture.png",dpi=150)
print('drawing successed!')
'''

def draw(name):
    fig = plt.figure(figsize=(12, 9), dpi=200)
    pricelog(name)
    xmajorLocator = MultipleLocator(1)
    ax1 = fig.add_subplot(111)
    ax1.xaxis.set_major_formatter(mdate.DateFormatter('%H:%M'))  # 设置时间标签显示格式
    plt.xticks(pandas.date_range(date[0], date[-1], freq='60min'))  # 时间间隔
    plt.xticks(rotation=90)
    plt.xticks(fontsize=10)
    ax1.set_xlabel('Time', size=15)
    ax1.set_ylabel('Price/¥', size=15)
    ax1.set_title(name.upper() + ' Price Daily' + '\n' + nowtime, size=20)
    ax1.plot(x, y, linewidth=1.0, label='price')
    ax1.plot(x, [average for obj in x], linewidth=1.0, label='average')
    ax1.legend(loc='upper right')
    ax1.grid(True)
    plt.savefig(os.getcwd() + '/data/'+ name + '.png', dpi=150)
    print('drawing successed!')
    return()

draw('btc')
draw('eth')
draw('ltc')
