#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'babo'

from optparse import OptionParser
import telnetlib,time,os
import types
import datetime


#get date
now = datetime.datetime.now()
day=now.strftime("%Y%m%d")

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
        print("ok")
    else:
        print("error")
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




