#!/usr/bin/env python
'''
This is python Script to Get A stock Alert daily through SMS
'''

from collections import namedtuple
import json

from twilio.rest import Client
import schedule
import time
import cookielib
import smtplib
import time
import urllib2


'''
This interface is for twilio.com account holder to get free sms alert
uncomment to use this interface/function

'''
'''
# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = "xxxxxxxxxxxxx"
auth_token = "yyyyyyyyyyyyyy"
client = Client(account_sid, auth_token)
'''
stock_change_dict = {}
stock_change_dict_1 = {}

try:
    from urllib.request import Request, urlopen
except ImportError:  # python 2
    from urllib2 import Request, urlopen




STOCK_NAME_ARRAY = [
    "INDEXBOM:SENSEX",
    "NSE:NIFTY",   
]

Stock = namedtuple("Stock", ["Index", "Current", "Change_pts", "Change_percent", "Updated_on"])

def Build_STOCK_Url():
    
    symbol_list = ','.join([stock for stock in STOCK_NAME_ARRAY])
    print symbol_list
    return 'http://finance.google.com/finance/info?client=ig&q=' \
    + symbol_list

def Get_STOCK_Content(url):
    
    req = Request(url)
    resp = urlopen(req)
    content = resp.read().decode('ascii', 'ignore').strip()
    content = content[3:]
    return content


def Parse_URL_Content(content):
    
    stock_resp_list = json.loads(content)

    list_stock = list()
    for stock_resp in stock_resp_list:
        isPositive = False if stock_resp["cp"] != None and len(stock_resp["cp"]) > 0 and stock_resp["cp"][0] == '-' else True

        stock_change_dict[stock_resp['t']] = stock_resp['c']
        stock_change_dict_1[stock_resp['t']] = stock_resp['cp']
        list_stock.append(Stock(stock_resp["t"], stock_resp["l"], stock_resp["c"], stock_resp["cp"], stock_resp["lt"]))

    return list_stock

'''
This is the way2sms interface is for free msg site to get Alert
'''

def sendsms(msg,Phone_Number):
    
    #way2sms user name
    User_Name = "xxxxxx"
    #way2sms password
    Password = "Fxxxx"  

    #Logging into the SMS Site
    url = 'http://site24.way2sms.com/Login1.action?'
    data = 'username='+User_Name+'&password='+Password+'&Submit=Sign+in'

    #For Cookies:
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

    # Adding Header detail:
    opener.addheaders = [('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36')]

    try:
       usock = opener.open(url, data)
    except IOError:
       return False

    jession_id = str(cj).split('~')[1].split(' ')[0]
    Send_SMS_Url = 'http://site24.way2sms.com/smstoss.action?'
    Send_SMS_Data = 'ssaction=ss&Token='+jession_id+'&mobile='+Phone_Number+'&message='+msg+'&msgLen=136'
    opener.addheaders = [('Referer', 'http://site25.way2sms.com/sendSMS?Token='+jession_id)]

    try:
       SMS_Sent_Page = opener.open(Send_SMS_Url,Send_SMS_Data)
    except IOError:
       return False
    return True


# added code to send sms 
'''
def sendSMS():
    print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
    print "message is sending..."
    myTwilioNumber = "+17xxxxxxx"
    destCellPhone = "+9189xxxxxx"
    msgIs="Hello, vinay BSE change = %s" % stock_change_dict['SENSEX']
    print msgIs
    client.messages.create(body = msgIs, from_=myTwilioNumber, to=destCellPhone)
'''

#if __name__ == "__main__":
def job():
    json_content = Get_STOCK_Content(Build_STOCK_Url())
    stock_list = Parse_URL_Content(json_content)
    Phone_Number = 'xxxxxx'  # Phone number
    msgIs="Hello, vinay Sensex change = %s and percentage  =%s , Nifty change = %s and percetage =%s" % (stock_change_dict['SENSEX'], stock_change_dict_1['SENSEX'], stock_change_dict['NIFTY'], stock_change_dict_1['NIFTY'])
    print msgIs
    sendsms(msgIs,Phone_Number)
    #sendSMS()


# Get Alert for 4 different timings 

schedule.every().day.at("09:20").do(job)
schedule.every().day.at("12:40").do(job)
schedule.every().day.at("01:20").do(job)
schedule.every().day.at("17:05").do(job)

#modify code according to your needs/scheduling
'''
#schedule.every(15).minutes.do(job)
#schedule.every().hour.do(sendSMS)
#schedule.every().day.at("10:30").do(job)
#schedule.every().day.at("12:30").do(job)
#schedule.every().day.at("15:50").do(job)
#schedule.every().monday.do(sendSMS)
#schedule.every().wednesday.at("13:15").do(sendSMS)
'''

while 1:
        schedule.run_pending()
        time.sleep(1)

