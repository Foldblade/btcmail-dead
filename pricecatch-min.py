#encoding:utf-8

import datetime
import pandas as pd
import urllib.request
import linecache

now = datetime.datetime.now()
now.strftime('%Y-%m-%d %H:%M:%S')
nowtime = now.strftime('%Y-%m-%d %H:%M:%S')
nowmin = now.strftime('%M')
print(nowtime)


url = "http://api.btctrade.com/api/ticker?coin=btc"
webdata = str(urllib.request.urlopen(url,timeout=10).read())
#抓取比特币价格网页

print(webdata)

a = int(webdata.find('"last":'))
#print(lastlocation)
b =int(webdata.find(',"vol"'))
#print(vollocation)
btcprice=webdata[int(a+7):int(b)]

if btcprice[0:1] == '"' :
    btcprice2=btcprice[1:]
    btcprice=btcprice2
#纠错,最原始的一个可能bug
print(btcprice)
#比特币价格提取


btcpriceold = linecache.getline('data/pricelog-min.csv',1441)
btcpriceold = btcpriceold[int(btcpriceold.find(','))+1:]
print('last price:' + btcpriceold)

print('now price:' + btcprice)

data=pd.read_csv('data/pricelog-min.csv')
data=data.drop(0)
data.to_csv('data/pricelog-min.csv',sep=",",index=False)
#删价格首行
f=open('data/pricelog-min.csv','a+')
f.write( nowtime + ',' + btcprice)
f.close()
#记录价格
print('record done!')

if nowmin == '00' :
    data = pd.read_csv('data/pricelog-monh.csv')
    data = data.drop(0)
    data.to_csv('data/pricelog-monh.csv', sep=",", index=False)
    # 删价格首行
    f = open('data/pricelog-monh.csv', 'a+')
    f.write(nowtime + ',' + btcprice)
    f.close()
    # 记录价格
#此段为日后升级开发打下基础
exit()
