#encoding:utf-8
import urllib.request
import linecache
import datetime
import matplotlib as mpl
mpl.use('Agg') #在非GUI下能够画图
import matplotlib.pyplot as plt
from matplotlib.ticker import  MultipleLocator
import matplotlib.dates as mdate
import smtplib  #加载smtplib模块
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import csv
import pandas
from bs4 import BeautifulSoup

now = datetime.datetime.now()
now.strftime('%Y-%m-%d %H:%M')
nowtime = now.strftime('%Y-%m-%d %H:%M')
print(nowtime)


url = "http://www.btctrade.com"
webdata = []
webdata = urllib.request.urlopen(url,timeout=15).read()
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

variance_sum = 0
for obj in pricelist :
    variance_min = (float(obj) - average)**2
    variance_sum = variance_sum + variance_min
variance = variance_sum / 1440
variance = round(variance,3)
print('variance=',variance)
#求方差

pricemax=max(pricelist)
pricemin=min(pricelist)
print(pricemax,pricemin)
range=float(pricemax)-float(pricemin)
range=round(range,3)
print('range=',range)
#求极差


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



message = MIMEMultipart()

# 第三方 SMTP 服务
mail_host = "smtp.xxxxxx.com"  # SMTP服务器
mail_user = "xxxx@xxxxxx.com"  # 用户名
mail_pass = "xxxxxxxxx"  # 密码

sender = 'service1@xxxxxxx.com'  # 发件人邮箱(最好写全, 不然会失败)
receivers = ['email1@email.com']  # 接收邮件，可设置多个，如['email1@email.com','email2@email.com']

content =   '<html>'+'运行时间:' + nowtime + '<br>'          \
          + '比特币价格:' + btcprice  + '<br>'    \
          + '24小时极差:'+ str(range) + '<br>'   \
          + '24小时方差:' + str(variance) + '<br>' \
          + '24小时平均值:' + str(average)+ '<br>' \
          + '24小时最大值:' + str(pricemax)+ '<br>'\
          + '24小时最小值:' + str(pricemin)+ '<br>'\
          + '技术支持:F.B.'</html>
#此content请用html写
title = '比特币价格:' + btcprice  # 邮件主题
message.attach(MIMEText(content, 'plain', 'utf-8'))  # 内容, 格式, 编码

message['From'] = "{}".format(sender)
message['To'] = ",".join(receivers)
message['Subject'] = title

with open('data/pricepicture.png', 'rb') as f:
    # 设置附件的MIME和文件名，这里是png类型:
    mime = MIMEBase('image', 'png', filename='pricepicture.png')
    # 加上必要的头信息:
    mime.add_header('Content-Disposition', 'attachment', filename='pricelog.png')
    mime.add_header('Content-ID', '<0>')
    mime.add_header('X-Attachment-Id', '0')
    # 把附件的内容读进来:
    mime.set_payload(f.read())
    # 用Base64编码:
    encoders.encode_base64(mime)
    # 添加到MIMEMultipart:
    message.attach(mime)
f.close()

try:
    smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
    smtpObj.login(mail_user, mail_pass)  # 登录验证
    smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
    print("mail has been send successfully.")
except smtplib.SMTPException as e:
    print(e)
