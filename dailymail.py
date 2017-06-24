# encoding:utf-8
import urllib.request
import requests
import os
import linecache
import datetime
import smtplib  #加载smtplib模块
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import mimetypes
import csv
import json

now = datetime.datetime.now()
nowtime = now.strftime('%Y-%m-%d %H:%M:%S')
print(nowtime)

where_script = os.path.split(os.path.realpath(__file__))[0]

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
# 检查设置

def priceget(coin):
    url = 'https://api.btctrade.com/api/ticker?coin=' + str(coin)
    response = requests.get(url, timeout=10).text
    # 抓取比特币价格网页
    js_dict = json.loads(response)
    return js_dict['last']

def  pricelog(coin):
    global x, date, y, pricelist, average, standard_deviation, range, variance, pricemax, pricemin
    with open( where_script + "/data/pricelog_min.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        date = [row['time'] for row in reader]
        csvfile.close()
    x = date
    with open( where_script + "/data/pricelog_min.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        pricelist = [row[ coin ] for row in reader]
        csvfile.close()
    y = pricelist

    sum = 0
    for obj in pricelist:
        sum = sum + float(obj)
    # print(sum)
    average = sum / 1442
    average = round(average, 3)
    print('average=', average)
    # 求平均值

    variance_sum = 0
    for obj in pricelist:
        variance_min = (float(obj) - average) ** 2
        variance_sum = variance_sum + variance_min
    variance = variance_sum / 1442
    standard_deviation = variance ** 0.5
    standard_deviation = round(standard_deviation, 3)
    variance = round(variance, 3)
    print('variance=', variance)
    print('standard deviation=', standard_deviation)
    # 求方差、标准差

    pricemax = float(str(max(pricelist)))
    pricemin = float(str(min(pricelist)))
    print(str(pricemax), str(pricemin))
    range = float(pricemax - pricemin)
    range = round(range, 3)
    print('Range=', range)
    # 求极差

    return (x, date, y, pricelist, average, standard_deviation, range, variance, pricemax, pricemin)

def outercontent(coin):
    pricelog(coin)
    contentpart ='''
<table border="0">
<tr><th colspan = "2" align="center">''' + str(coin.upper()) + '''</th></tr>
<tr><td>当前价格:</td><td>''' + str(priceget(coin)) + '''</td></th></tr>
<tr><td>24小时极差:</td><td>''' + str(range) + '''</td></th></tr>
<tr><td>24小时方差:</td><td>''' + str(variance) + '''</td></tr>
<tr><td>24小时标准差:</td><td>''' + str(standard_deviation) + '''</td></tr>
<tr><td>24小时平均值:</td><td>''' + str(average) + '''</td></tr>
<tr><td>24小时最大值:</td><td>''' + str(pricemax) + '''</td></tr>
<tr><td>24小时最小值:</td><td>''' + str(pricemin) + '''</td></tr>
</table><br>
'''
    return(contentpart)

f = open(where_script + '/mailsetting.json', 'r')
mailjson = json.load(f)
f.close()

def mailto(receivers):
    for people in receivers:
        print(people)
        message = MIMEMultipart()

        # 第三方 SMTP 服务
        smtp_host = mailjson["smtp_host"]  # SMTP服务器
        smtp_port = mailjson["smtp_port"]
        smtp_user = mailjson["smtp_user"]  # 用户名
        smtp_passwd = mailjson["smtp_passwd"]  # 密码

        sender = mailjson["sender"]  # 发件人邮箱(最好写全, 不然会失败)
        receiver = [people]
        print(receiver)

        content = '<html>'
        for coin in coins:
            content = content + outercontent(coin)
        content = content + '</html>'
        title = '比特币价格:' + str(priceget('btc'))  # 邮件主题
        message.attach(MIMEText(content, 'html', 'utf-8'))  # 内容, 格式, 编码

        message['From'] = "{}".format(sender)
        message['To'] = ",".join(receiver)
        message['Subject'] = title

        file_names = []
        for coin in coins:
            file_names.append(where_script + '/data/'+ coin +'.png')
        for file_name in file_names:
            data = open(file_name, 'rb')
            ctype, encoding = mimetypes.guess_type(file_name)
            if ctype is None or encoding is not None:
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)
            file_msg = MIMEBase(maintype, subtype)
            file_msg.set_payload(data.read())
            data.close()
            encoders.encode_base64(file_msg)  # 把附件编码
            basename = os.path.basename(file_name)
            file_msg.add_header('Content-Disposition', 'attachment', filename=basename)# 修改邮件头
            message.attach(file_msg)  # 设置根容器属性

        try:
            smtpObj = smtplib.SMTP_SSL(smtp_host, smtp_port)  # 启用SSL发信, 端口一般是465
            smtpObj.login(smtp_user, smtp_passwd)  # 登录验证
            smtpObj.sendmail(sender, receiver, message.as_string())  # 发送
            print(people + "'s mail has been send successfully.")
        except smtplib.SMTPException as e:
            print(e)
    return()


print(mailjson["receivers"])
mailto(mailjson["receivers"])
