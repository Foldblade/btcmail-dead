#encoding:utf-8
import urllib.request
import linecache
import datetime
import matplotlib as mpl
mpl.use('Agg') #在非GUI下能够画图
import matplotlib.pyplot as plt
from matplotlib.ticker import  MultipleLocator
import smtplib  #加载smtplib模块
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import csv
from bs4 import BeautifulSoup

now = datetime.datetime.now()
now.strftime('%Y-%m-%d %H:%M')
nowtime = now.strftime('%Y-%m-%d %H:%M')
print(nowtime)


url = "http://www.btctrade.com"
webdata = []
webdata = urllib.request.urlopen(url).read()
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


'''
udn = 0
f = open('data/pricelog-min-a.txt', 'r+')
line = f.readline()
while line:
    # print(line)
    a = int(line)
    udn = udn + int(a)
    # print(udn)
    line = f.readline()
f.close()
# 读取文件，涨为1，跌为-1。并求“绝对涨落”之和

# print(udn)
# “绝对涨落”之和

audn = udn / 3600
# print(audn)
# 求“绝对涨落”平均数

if audn < 0:
    suggestion = '以跌为主，不建议入手'
elif audn == 0:
    suggestion = '有涨又有落，相对持平'
elif 0 <= audn < 0.4:
    suggestion = '涨为主，涨的时间在全天比重不算长'
elif 0.4 >= audn:
    suggestion = '总趋势以涨为主，可以考虑卖出'
#print(suggestion)

# 给出建议
'''

message = MIMEMultipart()

# 第三方 SMTP 服务
mail_host = "smtp.yandex.com"  # SMTP服务器
mail_user = "email1@email.com"  # 用户名
mail_pass = "yourpasswd"  # 密码

sender = 'email1@email.com'  # 发件人邮箱(最好写全, 不然会失败)
receivers = ['email1@email.com','email2@email.com']  # 接收邮件，可设置多个，如['email1@email.com','email2@email.com']

content = '当前时间:' + nowtime + '\n' + '比特币价格:' + btcprice  + '\n' + '技术支持:F.B.'
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
