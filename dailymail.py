# encoding:utf-8
import urllib.request
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

now = datetime.datetime.now()
now.strftime('%Y-%m-%d %H:%M:%S')
nowtime = now.strftime('%Y-%m-%d %H:%M:%S')
nowmin = now.strftime('%M')
print(nowtime)


def priceget(name):
    url = "http://api.btctrade.com/api/ticker?coin=" + name
    webdata = str(urllib.request.urlopen(url, timeout=10).read())
    # 抓取比特币价格网页

    print(webdata)

    a = int(webdata.find('"last":'))
    # print(lastlocation)
    b = int(webdata.find(',"vol"'))
    # print(vollocation)
    price = webdata[int(a + 7):int(b)]

    if price[0:1] == '"':
        price2 = price[1:]
        price = price2
        # 纠错,最原始的一个可能bug
    # print(price)
    return (price)
    # 价格提取

def  pricelog(name):
    global x, date, y, pricelist, average, standard_deviation, range, variance, pricemax, pricemin
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

    variance_sum = 0
    for obj in pricelist:
        variance_min = (float(obj) - average) ** 2
        variance_sum = variance_sum + variance_min
    variance = variance_sum / 1440
    standard_deviation = variance ** 0.5
    standard_deviation = round(standard_deviation, 3)
    variance = round(variance, 3)
    print('variance=', variance)
    print('standard deviation=', standard_deviation)
    # 求方差、标准差

    pricemax = max(pricelist)
    pricemin = min(pricelist)
    print(pricemax, pricemin)
    range = float(pricemax) - float(pricemin)
    range = round(range, 3)
    print('Range=', range)
    # 求极差

    return (x, date, y, pricelist, average, standard_deviation, range, variance, pricemax, pricemin)

def outercontent(name):
    pricelog(name)
    contentpart ='''
<table border="0">
<tr><th colspan = "2" align="center">''' + str(name.upper()) + '''</th></tr>
<tr><td>当前价格:</td><td>''' +  priceget(name) + '''</td></th></tr>
<tr><td>24小时极差:</td><td>''' + str(range) + '''</td></th></tr>
<tr><td>24小时方差:</td><td>''' +str(variance) + '''</td></tr>
<tr><td>24小时标准差:</td><td>''' +str(standard_deviation) + '''</td></tr>
<tr><td>24小时平均值:</td><td>''' +str(average) + '''</td></tr>
<tr><td>24小时最大值:</td><td>''' +str(pricemax) + '''</td></tr>
<tr><td>24小时最小值:</td><td>''' +str(pricemin) + '''</td></tr>
</table>
'''
    return(contentpart)


def mailto(receivers):
    for people in receivers:
        print(people)
        message = MIMEMultipart()

        # 第三方 SMTP 服务
        mail_host = "smtp.email.com"  # SMTP服务器
        mail_user = "'email1@email.com'"  # 用户名
        mail_pass = "yourpassword"  # 密码

        sender = 'email1@email.com'  # 发件人邮箱(最好写全, 不然会失败)
        receiver = [people]
        print(receiver)

        content = '<html>' + outercontent('btc') + outercontent('eth') + outercontent('ltc') + '</html>'
        title = '比特币价格:' + priceget('btc')  # 邮件主题
        message.attach(MIMEText(content, 'html', 'utf-8'))  # 内容, 格式, 编码

        message['From'] = "{}".format(sender)
        message['To'] = ",".join(receiver)
        message['Subject'] = title

        file_names = [os.getcwd() + '/data/btc.png',os.getcwd() + '/data/eth.png',os.getcwd() + '/data/ltc.png']
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
            smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
            smtpObj.login(mail_user, mail_pass)  # 登录验证
            smtpObj.sendmail(sender, receiver, message.as_string())  # 发送
            print(people + "'s mail has been send successfully.")
        except smtplib.SMTPException as e:
            print(e)
    return()

mailto(['email1@email.com','email2@email.com'])
# 接收邮件，可设置多个并私密发送。如['email1@email.com','email2@email.com']


