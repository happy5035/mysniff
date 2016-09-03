# coding = utf-8
from scapy.all import *
from scapy.layers.http import HTTPRequest
from scapy.layers.inet import TCP
import threading
import time


import MySniffConf
from mysqlutils import mysql


def saveurltofile(urls):
    index = 0
    while 1:
        print 'run'
        time.sleep(2)
        if len(urls):
            with open(MySniffConf.urlfiles, 'a') as f:
                uls = urls[index:]
                print uls
                for url in uls:
                    f.write(url + '\n')
                    index += 1
    pass

class My_Sniff():
    def filterhandle(self, x):
        if x.haslayer(TCP) and (x.getlayer(TCP).dport == 80):
            return 1
        return 0

    def prnhandle(self, x):
        if x.haslayer(HTTPRequest):
            request = x.getlayer(HTTPRequest)
            Host = self.getfieldval(request, "Host")
            Path = self.getfieldval(request, "Path")
            url = Host + Path
            print url
            if self.sites.get(Host) is not None:
                self.save_to_database(url)
            else:
                keys = self.sites.keys()
                for key in keys:
                    if Host.find(key) != -1:
                        self.save_to_database(url)

    def save_to_database(self, url):
        count = self.mysql.query(url)
        print count
        if count == 0:
            self.mysql.insert(url)

    def getfieldval(self, pkt, attr):
        try:
            if pkt.getfieldval(attr) is None:
                return ''
            return pkt.getfieldval(attr)
        except AttributeError:
            return ''
        pass

    def __init__(self):
        self.sites = self.webhostfilereader()
        self.urls = set()
        self.urls_list = []
        self.mysql = mysql()

    def run(self):
        sniff(iface=MySniffConf.iface, prn=self.prnhandle, lfilter=self.filterhandle)  # , prn=prnhandle)

    def webhostfilereader(self):
        filepath = MySniffConf.webhostconf
        f = open(filepath)
        sites = {}
        try:
            for line in f.readlines():
                start = line.find('#')
                if start != -1:
                    continue
                line = line.replace('\n', '')
                sites[line] = line
        finally:
            f.closed
        return sites




if __name__ == '__main__':
    My_Sniff().run()
