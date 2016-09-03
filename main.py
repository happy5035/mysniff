# coding = utf-8
from scapy.all import *
from scapy.error import Scapy_Exception
import sys
from scapy.layers.inet import *
from arp_poison import arp_poison


def mysniff():

    pass


def main():
    arp_poison().poison()
    mysniff()
    


if __name__ == '__main__':
    main()

    # mysniff()
    # print RandNum(10,20)
    pass