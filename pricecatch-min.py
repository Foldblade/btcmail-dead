#encoding:utf-8

from bs4 import BeautifulSoup
import datetime
import pandas as pd
import urllib.request
import linecache

now = datetime.datetime.now()
now.strftime('%Y-%m-%d %H:%M:%S')
nowtime = now.strftime('%Y-%m-%d %H:%M:%S')
print(nowtime)


url = "http://www.btctrade.com"
webdata = []
webdata = urllib.request.urlopen(url,timeout=10).read()
soup = BeautifulSoup(webdata,"html.parser")
priceline = str(soup.find(id="rate-btc"))
#抓取比特币价格网页

print(priceline)
a = int(priceline.find('">'))
#print(btclocation)
b =int(priceline.find('</i>'))
#print(ltclocation)
btcprice=priceline[int(a+2):int(b)]

if btcprice[0:1] == '"' :
  btcprice2=btcprice[1:5]
  btcprice=btcprice2
#纠错，初代常会报错，貌似现在不会出现此问题

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
