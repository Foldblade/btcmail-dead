#encoding:utf-8
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import datetime
from matplotlib.ticker import  MultipleLocator
import matplotlib.dates as mdate
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd
import csv

now = datetime.datetime.now()
now.strftime('%Y-%m-%d %H:%M')
nowtime = now.strftime('%Y-%m-%d %H:%M')
print(nowtime)

with open("data/pricelog-min.csv") as csvfile :
  reader = csv.DictReader(csvfile)
  x = [row['Time'] for row in reader]
with open("data/pricelog-min.csv") as csvfile:
  reader = csv.DictReader(csvfile)
  y = [row['Price'] for row in reader]
#print(x)
#print(y)

#xmajorLocator = MultipleLocator(1)
xmajorLocator = MultipleLocator(1)
plt.figure(dpi=300)
plt.title('BTC Price Daily'+'\n'+ nowtime, size=14)
plt.xlabel('Time/min', size=14)
plt.ylabel('Price/¥', size=14)
plt.plot(y,linewidth=1.0,)
plt.grid(True)
plt.savefig("data/pricepicture.png",dpi=300)
print('success!')

