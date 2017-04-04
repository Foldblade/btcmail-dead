#encoding:utf-8

#这是邮件附图绘图的代码，dailymail里也有，单独发一遍。

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


with open("data/pricelog-min.csv") as csvfile :
  reader = csv.DictReader(csvfile)
  date = [row['Time'] for row in reader]
  csvfile.close()
x = date
with open("data/pricelog-min.csv") as csvfile:
  reader = csv.DictReader(csvfile)
  pricelist = [row['Price'] for row in reader]
  csvfile.close()
y = pricelist

sum = 0
for obj in pricelist :
    sum = sum + float(obj)
#print(sum)
average = sum / 1440
average = round(average,3)
print('average=',average)
#求平均值


xmajorLocator = MultipleLocator(1)
fig=plt.figure(figsize=(12,9),dpi=300)
ax1=fig.add_subplot(111)
ax1.xaxis.set_major_formatter(mdate.DateFormatter('%H:%M'))#设置时间标签显示格式
plt.xticks(pandas.date_range(date[0],date[-1],freq='60min'))#时间间隔
plt.xticks(rotation=90)
plt.xticks(fontsize = 10)
ax1.set_xlabel('Time', size=15)
ax1.set_ylabel('Price/¥', size=15)
ax1.plot(x,y,linewidth=1.0,label='price')
ax1.plot(x,[average for obj in x],linewidth=1.0,label='average')
plt.legend(loc='upper right')
plt.title('BTC Price Daily'+'\n'+ nowtime, size=25)
plt.grid(True)
plt.savefig("data/pricepicture.png",dpi=300)
print('drawing successed!')
