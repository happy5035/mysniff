# coding = utf-8
import threading
from scapy.sendrecv import sendp
from scapy.volatile import RandNum

import MySniffConf
import thread

class task(threading.Thread):
    def __init__(self, pkg):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.pkg = pkg
        pass
    def run(self):
        sendp(self.pkg,inter=RandNum(2, 5), loop=1,verbose=0)

