# coding=utf-8
import MySQLdb
import hashlib
import requests


# 数据库连接参数
class mysql:
    def __init__(self):
        self.conn = MySQLdb.connect(db="sniff", user="root", passwd="admin", host="127.0.0.1", port=3306)
        self.cur = self.conn.cursor()

    def execute(self, sql):
        try:
            result = self.cur.execute(sql)
            self.conn.commit()
        except:
            self.conn.roolback()
        return result

    def insert(self, url):
        _hash = self.gethash(url)
        sql = "insert into url (hash,url) values('%s','%s')" % (_hash, url)
        return self.execute(sql)

    def gethash(self, url):
        md5 = hashlib.md5()
        md5.update(url)
        _hash = md5.hexdigest()
        print _hash
        return _hash

    def query(self, url):
        _hash = self.gethash(url)
        sql = "select * from url where hash = '%s'" % (_hash)
        return self.execute(sql)

    def getall(self):
        sql = 'select * from url'
        try:
            self.cur.execute(sql)
            return self.cur.fetchall()
        except:
            print "Error: unable to fecth data"

    def get_image(self, result):
        if result:
            for id, h, url, path, state in result:
                res = requests.get('http://' + url)
                headers = res.headers
                ct = headers.get('Content-Type')
                print ct
                t = ct.split('/')
                if len(t) > 1:
                    _type = t[1]
                    path = '/tmp/test/' + h + '.' + _type
                    print 'download image ' + path
                    if _type == 'hevc':
                        self.update(id, '', 1)
                        continue
                    with open(path, 'wb') as f:
                        f.write(res.content)
                    self.update(id, path, 1)

    def update(self, id, path, state):
        try:
            sql = "update url set path ='%s',state=%s " \
                  "where id = %s" % (path, state, id)
            result = self.cur.execute(sql)
            self.conn.commit()
            return result
        except:
            print 'update data error'
            self.conn.roolback()

    def download_image(self):
        sql = 'select * from url where state = 0'
        try:
            self.cur.execute(sql)
            result = self.cur.fetchall()
            self.get_image(result)
        except:
            print "Error: unable to fecth data"


if __name__ == '__main__':
    s = mysql()
    s.download_image()
