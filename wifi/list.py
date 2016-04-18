#!/usr/bin/env python
# -*- coding:utf-8 -*-
import web
import json
import MySQLdb

urls = (
    "/", "index",
    "/getWifi", "queryWifi"
)

# static
render = web.template.render('static', cache=False)

class index:
    def GET(self):
        return render.index("static")


class queryWifi:
    def POST(self):
        mysql = Database()
        page = int(web.input().get("page"))
        rows = int(web.input().get("rows"))
        limitCount = (page - 1) * rows
        data = mysql.query("SELECT * FROM keydata order by createtime desc limit " + str(limitCount) + "," + str(rows) + ";")
        length = mysql.query("SELECT id FROM keydata")
        WifiStr = []
        for row in data:
            thisIp = row['ip']
            thisSsid = str(row['ssid'].encode('utf-8'))
            thisTime = str(row['createtime'])
            thiskey = str(row['password'])
            thisCountry = str(row['country'].encode('utf-8'))
            thisProvince = str(row['province'].encode('utf-8'))
            thisCity = str(row['city'].encode('utf-8'))
            thisIsp = str(row['isp'].encode('utf-8'))
            thisId = str(row['id'])

            WifiStr.append({"ip": thisIp, "id": thisId, "time": thisTime, "key": thiskey, "ssid": thisSsid,"country":thisCountry,"province":thisProvince,"city":thisCity,"isp":thisIsp})

        return '{"rows":' + json.dumps(WifiStr) + ',"total":' + str(len(length)) + '}'

class Database:
    host = '127.0.0.1'
    user = 'root'
    password = 'root'
    db = 'ttlwifi'
    charset = 'utf8'

    def __init__(self):
        self.connection = MySQLdb.connect(
            self.host, self.user, self.password, self.db, charset=self.charset)
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

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
