#!/usr/bin/python

from requests import session
from bs4 import BeautifulSoup
import re
import datetime
import socket
import cookielib
import sys
import smtplib
import time
import urllib2
from getpass import getpass
import schedule


def sendsms(msg,Phone_Number):
    User_Name = "xxxxxxx"
    Password = "yyyyyy"
    
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

    


def Is_Today_bday() :
# intial code for friends birtday wisher 

    bday_list = {}

    
    with open('DOB_Name_List.txt', 'r') as R:
        for line in R:
            l = line.strip().split()  # split the line to list
            bday_list[l[0]] = {k:v for k,v in zip(l[1::2], l[2::2])}

# To check dictionary created properly
#print bday_list


#    for key in bday_list:
#        print bday_list[key].values()[1] #[0]

#    print time.strftime("%x")[:5] + key
#    print "key: " + key + "\t" + "value " + bday_list[key]


# To check present date with list in dictionary if matches send msg to wish
    
    for key in bday_list:
        if time.strftime("%x")[:5] == key :
            print 'Happy Birthday %s\t PH:%s ' % (bday_list[key].values()[1],bday_list[key].values()[0])
            msg = 'Happy birthday ' +  bday_list[key].values()[1]
            Phone_Number = bday_list[key].values()[0]
            #send_sms(msg,Phone_Number)
            sendsms(msg,Phone_Number)
            print 'called send_sms'
        else:
			print 'NO'
        


#if __name__ == '__main__':
def job():
    Is_Today_bday()
    
# scheduler to check Bday_list everyday and send SMS to wish
#schedule.every(1).minutes.do(job)
#schedule.every().hour.do(sendSMS)
schedule.every().day.at("6:30").do(job)
#schedule.every().day.at("12:30").do(job)
#schedule.every().day.at("19:47").do(job)
#schedule.every().monday.do(sendSMS)
#schedule.every().wednesday.at("13:15").do(sendSMS)

while 1:
        schedule.run_pending()
        time.sleep(1)


