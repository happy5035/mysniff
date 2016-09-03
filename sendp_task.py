# coding = utf-8
import threading
from scapy.sendrecv import sendp
from scapy.volatile import RandNum

import MySniffConf


class task(threading.Thread):
    def __init__(self, pkg):
        threading.Thread.__init__(self)
        self.pkg = pkg
        pass
    def run(self):
        sendp(self.pkg,inter=RandNum(10, 20), loop=1)

