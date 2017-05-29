# encoding:utf-8

import datetime
import pandas as pd
import urllib.request
import linecache

now = datetime.datetime.now()
now.strftime('%Y-%m-%d %H:%M:%S')
nowtime = now.strftime('%Y-%m-%d %H:%M:%S')
nowmin = now.strftime('%M')
print(nowtime)


def priceget(name):
  url = "http://api.btctrade.com/api/ticker?coin=" + name
  webdata = str(urllib.request.urlopen(url,timeout=10).read())
  #抓取比特币价格网页
  
  print(webdata)
  
  a = int(webdata.find('"last":'))
  #print(lastlocation)
  b = int(webdata.find(',"vol"'))
  #print(vollocation)
  price = webdata[int(a+7):int(b)]
  
  if price[0:1] == '"' :
    price2=price[1:]
    price=price2
    #纠错,最原始的一个可能bug
  #print(price)
  return(price)
  #价格提取

btcprice = priceget('btc')
ethprice = priceget('eth')
ltcprice = priceget('ltc')
print(btcprice)
print(ethprice)
print(ltcprice)
#结果输出


data=pd.read_csv('data/pricelog-min.csv')
data=data.drop(0)
data.to_csv('data/pricelog-min.csv',sep=",",index=False)
#删价格首行
f=open('data/pricelog-min.csv','a+')
f.write( nowtime + ',' + btcprice + ',' + ethprice + ',' + ltcprice)
f.close()
#记录价格
print('record done!')
