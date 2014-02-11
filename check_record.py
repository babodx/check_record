#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'babo'

from optparse import OptionParser
import telnetlib,time,os
import types
import datetime
import smtplib
from email.mime.text import MIMEText

#get date
now = datetime.datetime.now()
day=now.strftime("%Y%m%d")

#mail config
mailto_list=["XXX@xxx.com"]
mail_host="smtp.hysec.com"  #设置服务器
mail_user="user"    #用户名
mail_pass="pwd"   #口令
mail_postfix="domain.com"  #发件箱的后缀

def send_mail(to_list,sub,content):
    me="<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content,_subtype='plain',_charset='utf-8')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_user,mail_pass)
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception, e:
        print str(e)
        return False

def check(host,user):
    now = datetime.datetime.now()
    day=now.strftime("%Y%m%d")
    tn = telnetlib.Telnet(host,'23')
    tn = telnetlib.Telnet(host)
    #login
    tn.read_until(b"login:")
    tn.write(user.encode('UTF-8') + b"\n")
    #run command
    tn.read_until(b'#')
    #print("login success")
    command='ls /udisk/record| grep '+day

    tn.write(command.encode('UTF-8')+b"\r\n")
    result=tn.read_until(b'#',50)
    if (result.__len__() > 60):
        send_mail(mailto_list,"check_record "+host+" success",host+" check status ok")
    else:
        send_mail(mailto_list,"check_record "+host+" fail",host+" check status error")
    #close
    tn.close() # tn.write('exit\n')

def main():
    parser= OptionParser(
        # prog=u"check_record host user",usage="%prog",
        # description=u'检查host下面/udisk/record是否有当天录音。'
        prog = 'check_record.py HOST USER', usage='%prog',
        description= ''
        )




    (options, args) = parser.parse_args()

    if len(args)==2:
        host = args[0]
        user = args[1]
        check(host,user)
    else:
        parser.print_help()


if __name__=="__main__":
    main()




